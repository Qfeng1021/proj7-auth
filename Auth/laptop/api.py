# Laptop Service
from passlib.apps import custom_app_context as pwd_context
from flask import Flask, request, make_response, render_template, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import os
import time
from itsdangerous import (TimedJSONWebSignatureSerializer \
                                  as Serializer, BadSignature, \
                                  SignatureExpired)

app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "test1234@#$"
app.config["LENGTH"] = 0
api = Api(app)

client = MongoClient("db", 27017)
db = client.tododb

def hash_password(password):
    return pwd_context.encrypt(password)

def verify_password(password, hashVal):
    return pwd_context.verify(password, hashVal)

def generate_auth_token(_id, expiration=600):
   s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
   # pass index of user
   return s.dumps({'id': _id})

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token
    return True
class index(Resource):
    def get(self):
        app.logger.debug("Register")
        return make_response(render_template("register.html"))

def top_k():
    top = request.args.get("top")
    if top:
        item = db.tododb.find({"open": {"$exists": True}}).limit(int(top))
    else:
        item = db.tododb.find({"open": {"$exists": True}})
    return item


def find_and_append(item, item_list):
    dictionary = {}
    for key in item_list:
        dictionary[key] = []
    for i in item:
        for key in item_list:
            try:
                dictionary[key].append(i[key])
            except KeyError:
                return "Empty"
    return dictionary


def find_and_add(item,item_list):
    csv = ""
    for key in item_list:
        csv += key + " "
    csv += ": "
    for i in item:
        for key in item_list:
            try:
                csv += key + ": " + i[key] + " "
            except KeyError:
                return "Empty"
        csv += "|| "
    return csv

class Laptop(Resource):
    def get(self):
        return {
            'Laptops': ['Mac OS', 'Dell',
            'Windozzee',    'Yet another laptop!',
	    'Yet yet another laptop!'
            ]
        }

class listAll(Resource):
    def get(self):
        item = top_k()
        item_list = ["open", "close"]
        open_close = find_and_append(item, item_list)
        return open_close

class register(Resource):
    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")
        item = db.tododb.find_one({"username" : username})
        if username is None or password is None:
            return "Bad Request", 400
        elif item is not None:
            return "Bad Request: The username already exist.", 400
        else:
            password = hash_password(str(password))
            app.config["LENGTH"] = app.config["LENGTH"] + 1
            _id = app.config["LENGTH"]
            item = {"username" : username, "password" : password, "Location" : _id}
            db.tododb.insert_one(item)
            return {"username" : username, "Location" : _id}, 201


class userRequest(Resource):
    def get(self, _id):
        item = db.tododb.find_one({"Location" : _id})
        if _id is None or item is None:
            return "Bad request", 400
        else:
            return {"username" : item["username"], "Location" : item["Location"]}


class token(Resource):
    def get(self):
        username = request.args.get("username")
        password = request.args.get("password")
        item = db.tododb.find_one({"username": username})
        app.logger.debug(username)
        app.logger.debug(password)
        if username is None or password is None:
            return "Bad Request", 400
        elif item is None:
            return "Unauthorized : There is no such username.", 401
        elif verify_password(password, item["password"]) is False:
            return "Unauthorized : Incorrect password.", 401
        else:
            _token = generate_auth_token(item["Location"], 300)
            return make_response(jsonify({"token" : _token.decode('ascii'), "duration" : 300}), 201)




class listAllCsv(Resource):
    def get(self):
        item_list = ["open", "close"]
        item = top_k()
        all_csv = find_and_add(item, item_list)
        return all_csv


class listOpenOnly(Resource):
    def get(self):
        item_list = ["open"]
        item = top_k()
        open = find_and_append(item, item_list)
        return open

class listOpenOnlyCsv(Resource):
    def get(self):
        item_list = ["open"]
        item = top_k()
        open_csv = find_and_add(item, item_list)
        return open_csv


class listCloseOnly(Resource):
    def get(self):
        item_list = ["close"]
        item = top_k()
        close = find_and_append(item, item_list)
        return close

class listCloseOnlyCsv(Resource):
    def get(self):
        item_list = ["close"]
        item = top_k()
        close_csv = find_and_add(item, item_list)
        return close_csv


# Create routes
# Another way, without decorators
api.add_resource(Laptop, '/')
api.add_resource(index, '/api')
api.add_resource(register, '/api/register')
api.add_resource(userRequest, '/api/users/<int:_id>')
api.add_resource(token, '/api/token')
api.add_resource(listAll, '/listAll', '/listAll/json')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/json')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/json')

api.add_resource(listAllCsv, '/listAll/csv')
api.add_resource(listOpenOnlyCsv, '/listOpenOnly/csv')
api.add_resource(listCloseOnlyCsv, '/listCloseOnly/csv')
# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
