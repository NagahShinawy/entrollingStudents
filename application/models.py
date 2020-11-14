from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

now = datetime.now()


class User(db.Document):
    user_id = db.IntField(unique=True)
    fname = db.StringField(max_length=50)
    lname = db.StringField(max_length=50)
    email = db.EmailField(unique=True)
    password = db.StringField()

    def __str__(self):
        return self.fname

    def set_password(self, password):
        # set hashed password to user
        self.password = generate_password_hash(password)

    def get_password(self, password):
        # self.password ==> saved on db
        # password ==>  passed by the use from form
        return check_password_hash(self.password, password)


class Blog(db.Document):
    blog_id = db.IntField(unique=True)
    title = db.StringField(max_length=100)
    content = db.StringField(max_length=300)
    created = db.DateTimeField(default=now)


class Course(db.Document):
    course_id = db.IntField(unique=True)
    title = db.StringField(max_length=100)
    desc = db.StringField(max_length=300)
    credits = db.IntField()
    terms = db.StringField(max_length=100)


class Enrollment(db.Document):
    # many2many relationship between User and Course
    # so enrollment must be at third collection "table" to know which course that user join to
    user_id = db.IntField(unique=False)
    course_id = db.IntField(unique=False)


class Account(db.Document):
    _id = db.ObjectIdField()
    joined = db.DateTimeField(default=now)
    increment = db.SequenceField()
