from flask import (render_template, request,
                   jsonify, Response, redirect, url_for, flash, session)
from . import app
from .forms import LoginForm, RegisterForm
from .models import User, Blog, Account, Course, Enrollment
from datetime import datetime
import json
from .apis import *

from .piplines import course_enrollments
from .utils import is_authenticated

now = datetime.now()


_courses = [
        {"course_id": 111, "title": 'PHP', "desc": 'Web Backend', "credits": 3, "terms": "Far, Spring"},
        {"course_id": 222, "title": 'Django', "desc": 'Web Backend Python', "credits": 65, "terms": "Full Feature Web"},
        {"course_id": 333, "title": 'Flask', "desc": 'Web Micro', "credits": 4, "terms": "Fast & Micro Framework"},
        {"course_id": 444, "title": 'Flutter', "desc": 'Mobile', "credits": 8, "terms": "Mobile Development"},
        {"course_id": 555, "title": 'Java', "desc": 'Web Mobile Desktop', "credits": 9, "terms": "Many Scopes"},
        {"course_id": 666, "title": 'IOS', "desc": 'Mobile Development IOS Platform', "credits": 43, "terms": "Apple"},
        ]


@app.route('/')
@app.route('/home', strict_slashes=False)
@app.route('/index', strict_slashes=False)
def index():
    url = request.path
    if 'home' in url:
        return "<h1 style='color:red;'> Flask App Home<h1>"

    if 'index' in url:
        return "<h1 style='color:green;'> Flask App index<h1>"

    return "<h1> Flask App<h1>"


@app.route('/myhome', strict_slashes=False)
@app.route('/myindex', strict_slashes=False)
def myindex():
    is_auth = is_authenticated()
    return render_template('index.html',
                           name=request.user_agent, date=now,
                           request=request, nagah=True, is_auth=is_auth)


@app.route('/login', methods=['GET', 'POST'])
def login():
    is_auth = is_authenticated()
    if session.get('username'):
        return redirect(url_for('myindex', is_auth=is_auth))
    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            form = LoginForm(request.form)
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.objects.filter(email=email).first()
            if user and user.get_password(password):
                flash(f" '{user.fname}' You are logged in", 'success')
                # flash("You are logged in", 'error') # testing error
                session['user_id'] = user.user_id
                session['username'] = user.fname
                is_auth = is_authenticated()
                return redirect(url_for("myindex", is_auth=is_auth))  # myindex is function name not route
        # todo: use else in case of errors or use errors in html forms (both work)
            else:
                flash("Invalid username or password", 'danger')
            # errors = []
            # print(form.errors)
            # # flash("You have some errors, try again !", 'error')  # hard coded
            # for field, error in form.errors.items():
            #     errors.append("".join(error))
            # print(errors)
            # # list errors on web page
            # for err in errors:
            #     flash(err, 'danger')
    return render_template('login.html', date=now, form=form, is_auth=is_auth)


@app.route('/logout')
def logout():
    username = session['username']
    session['username'] = False  # remove username from sessions
    session.pop('user_id', None)  # remove user_id from sessions
    is_auth = is_authenticated()
    flash(f'Hope coming Back {username}', 'success')
    return redirect(url_for('login', is_auth=is_auth))


@app.route('/forget_password')
def forget_password():
    return render_template('forget-password.html')


@app.route('/users/<int:user_id>')
def user_profile(user_id):
    users = range(10, 20)

    return render_template('index.html', users=users, date=now)


@app.route('/courses/delete/', methods=['POST'])
def delete_enroll():
    course_id = request.form['course_id']
    user_id = session.get('user_id')
    # pk of "Enrollment" is ===> course_id and user_id BOTH
    course_enrolled = Enrollment.objects.get(course_id=course_id, user_id=user_id)
    course = Course.objects.get(course_id=course_id)
    course_enrolled.delete()
    flash(f' "{course.title}" Deleted Successfully', 'success')
    return redirect(url_for('enroll'))


@app.route('/register',  strict_slashes=False, methods=['GET', 'POST'])
def register():
    is_auth = is_authenticated()
    if is_auth:
        return redirect(url_for('myindex'))
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            # last_user = User.objects.order_by('-user_id')[0]  # way 1
            countusers = User.objects.count()   # way 2
            user_id = countusers + 1
            data = request.form
            email = data.get('email')
            fname = data.get('fname')
            lname = data.get('lname')
            password = data.get('password')
            newuser = User(user_id=user_id, email=email, fname=fname, lname=lname)
            newuser.set_password(password)
            newuser.save()
            flash(f" '{newuser.fname.title()}' Register Successfully, Login Now", 'success')
            return redirect(url_for("login", is_auth=is_auth))
        else:
            flash("Errors", 'danger')
    return render_template('register.html', date=now, form=form, is_auth=is_auth)


@app.route('/enroll/',  strict_slashes=False, methods=['GET', 'POST'])
def enroll():
    is_auth = is_authenticated()
    if not is_auth:
        flash('You Should Login First', 'warning')
        return redirect(url_for('login', is_auth=is_auth))
    print(request.form)  # In case of form post
    print(request.data)  # In case of POST
    print(request.args)  # In case of GET
    user_id = session['user_id']
    if request.method == 'POST':
        # captured from form
        course_id = request.form['course_id']
        course_title = request.form['course_title']
        terms = request.form['terms']
        data = {"course_id": course_id, "course_title": course_title, "terms": terms}
        # data = **request.form
        # **request ==> means ==> course_id=course_id, course_title=course_title
        enrollobj = Enrollment.objects(user_id=user_id, course_id=course_id)
        if enrollobj:
            flash(f'You are Already Joined "{course_title}" ', 'warning')
            return redirect(url_for('courses', is_auth=is_auth))
        else:
            Enrollment(user_id=user_id, course_id=course_id).save()
            flash(f'Successfully Joined to "{course_title}" ', 'success')
    # enrolls = Enrollment.objects.filter(user_id=user_id)
    # courses_ids = []
    # for enr in enrolls:
    #     courses_ids.append(enr.course_id)
    #
    # classes = [Course.objects.get(course_id=_id) for _id in courses_ids]
    course_enrollments[4]['$match']['user_id'] = user_id
    _users = list(User.objects.aggregate(*course_enrollments))
    print(_users)
    classes = [_user['courses'] for _user in _users]
    return render_template('enrollment.html',  date=now, classes=classes, is_auth=is_auth)


@app.route('/contact',  strict_slashes=False)
def contact():
    return render_template('contact.html', contact=True, date=now)


@app.route('/service',  strict_slashes=False)
def service():
    return render_template('service.html', service=True, date=now)


@app.route('/post', methods=['GET', 'POST'],  strict_slashes=False)
def post():
    from pandas import DataFrame
    data: bytes = request.data  # post request
    args = request.args  # get request

    # post request
    if data:
        print("Data", data)
        data: dict = json.loads(data)
        DataFrame(data, index=[0]).to_excel('names.xlsx')

    # get request
    if args:
        print("args", args)
        DataFrame(args, index=[0]).to_excel('names.xlsx')
    return render_template('post.html', post=True, date=now)


@app.route('/courses',  strict_slashes=False)
@app.route('/courses/<term>',  strict_slashes=False)
def courses(term="DefaultValue"):
    # qs = Course.objects.order_by('+course_id')  # + means Asc , - means Desc
    qs = Course.objects.order_by('-course_id')  # + means Asc , - means Desc
    return render_template('courses.html', date=now, courses=qs, term=term)


@app.route('/courses/<int:course_id>',  strict_slashes=False)
def course_profile(course_id=1):
    # course_data = None
    # for course in _courses:
    #     if course_id == course['course_id']:
    #         course_data = course
    try:
        course = Course.objects.get(course_id=course_id)
    except Exception:
        return render_template('404.html')
    return render_template('course.html', course=course, date=now)


# wat 1 to return json obj
@app.route('/api/',  strict_slashes=False)
def api():
    return jsonify(_courses[:3])


# wat 2 to return json obj
@app.route('/api-2/',  strict_slashes=False)
def api2():
    response = app.response_class(
        response=json.dumps(_courses),
        status=200,
        mimetype='application/json'
    )
    return response


# wat 3 to return json obj
@app.route('/api-3/',  strict_slashes=False)
def api3():
    if _courses:
        data = _courses
    else:
        data = {'result': 'No items'}
    response = Response(json.dumps(data), mimetype='application/json', status=200)
    return response


@app.route('/api/<int:course_id>',  strict_slashes=False)
def single_course(course_id):
    for course in _courses:
        if course_id == course['course_id']:
            return jsonify(course), 200
    return jsonify({"result": "Not Found"}), 404


@app.route('/users', strict_slashes=False)
def users():
    userdata = {
        "user_id": 6,
        "fname": "Mahmoud",
        "lname": "Bibo",
        "email": "mido.bibo@yahoo.com",
        "password": "myPassword"}
    new_user = User(**userdata)
    try:
        new_user.save()
    except Exception as error:
        pass

    qs = User.objects.all()
    print(qs)
    return render_template('users.html', users=qs, date=now)


@app.route('/user/<int:user_id>', strict_slashes=False)
def user(user_id):
    obj = User.objects.filter(user_id=user_id)
    return render_template('user.html', user=obj, date=now)


@app.route('/blogs', strict_slashes=False)
def blogs():

    blog = Blog(blog_id=3, title="Basics Python", content="Python from zero to here")
    try:
        blog.save()
    except Exception as error:
        pass
    qs = Blog.objects.all()
    return render_template('blogs.html', date=now, blogs=qs)


@app.route('/accounts', strict_slashes=False)
def account():

    accountobj = Account()
    try:
        accountobj.save()
    except Exception as error:
        pass
    qs = Account.objects.all()
    print(qs)
    return render_template('accounts.html', date=now, accounts=qs)


@app.route('/nagah', strict_slashes=False)
def noga():
    return "Nagah"


@app.route('/api/delete/<int:user_id>', strict_slashes=False, methods=['DELETE'])
def delete(user_id):
    User.objects(user_id=user_id).delete()
    response = app.response_class(
        response=json.dumps({"result": "Deleted User"}),
        status=200,
        mimetype='application/json'
    )
    return response