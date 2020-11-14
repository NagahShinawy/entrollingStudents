from flask_restplus import Resource
from application import api, app
from flask import jsonify, make_response, Response, request
from werkzeug.security import generate_password_hash
from .models import *
import json


@api.route('/api-flask-restplus', '/api-flask-restplus/')
class UsersAPI(Resource):

    def get(self):
        return jsonify(User.objects.all()), 200

    def post(self):
        # data = api.payload  # use it , it does the same .
        data = request.data
        if not data:
            return {'result': 'missing data'}, 400
        data = json.loads(data)
        try:
            user_id = User.objects.count() + 1
            fname = data.get('fname')
            lname = data.get('lname')
            email = data.get('email')
            password = data.get('password')
            password2 = data.get('password2')
            if password != password2:
                return {'result': 'invalid match passwords'}, 400
            newuser = User(user_id=user_id, fname=fname, lname=lname, email=email, password=password)
            newuser.set_password(password)
            newuser.save()
        except Exception as err:
            return {'result': str(err)}, 400
        return make_response(jsonify(newuser), 200)


@api.route('/api-flask-restplus/<int:user_id>', '/api-flask-restplus/<int:user_id>/')
class UserAPI(Resource):

    def get(self, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except Exception as err:
            return {'result': 'not found'}, 404
            # return jsonify({'result': 'not found'}), 404
            # return Response('not found', mimetype='application/json', status=404)
        # return jsonify(user), 200
        return make_response(jsonify(user), 200)

    def put(self, user_id):
        data = api.payload
        try:
            user = User.objects(user_id=user_id)  # BaseQuerySet obj
            # user = User.objects.get(user_id=user_id)   # User obj
        except Exception as err:
            return {'result': 'not found'}, 404

        try:
            password = data.get('password')  # hashing password
            print(password)
            if password:
                data['password'] = generate_password_hash(password)
            user[0].update(**data)
            print(data)
        except Exception as err:
            return {'result': str(err)}
        return make_response(jsonify(user), 202)

    def delete(self, user_id):
        User.objects(user_id=user_id).delete()
        # return jsonify({"result": "user is deleted !"}), 204
        return jsonify({"result": "user is deleted !"})
        # resp = make_response(jsonify({"result": "deleted"}), 204)
        # try:
        #     user = User.objects.get(user_id=user_id)
        #     user.delete()
        #     # return make_response({"result": "deleted"}, 204)
        #     # return {'result': 'deleted'}, 204
        #     response = app.response_class(
        #         response={"result": "Deleted"},
        #         status=204,
        #         mimetype='application/json'
        #     )
        #     return response
        # except Exception as err:
        #     return {'result': 'not found ' + str(err)}, 404


@api.route('/hello', '/hello/')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}