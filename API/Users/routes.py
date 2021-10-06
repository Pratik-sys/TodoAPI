import json
import bleach
from flask import jsonify, request
from flask_restx import Resource, Namespace
from API import bcrypt
from API.models import User
from API.validation import validateUserDetails
from flask_jwt_extended import create_access_token

users = Namespace("users")

@users.route("/register")
class RegisterUser(Resource):
    def post(self):
        record = json.loads(request.data)
        try:
            hashed_password = bcrypt.generate_password_hash(
                bleach.clean(record["password"])
            ).decode("utf-8")
            user = User(
                name=bleach.clean(record["name"]),
                nickname=bleach.clean(record["nickname"]),
                email=record["email"],
                password=hashed_password,
            )
            errors = validateUserDetails(user)
            if len(errors) == 0:
                user.save()
                return jsonify({"Msg": "User added sucessfully"}, 200)
            else:
                return jsonify(errors, 404)
        except Exception as ex:
            return jsonify({"Msg": "Error while adding user to the database"}, 500)


@users.route("/login")
class LoginUser(Resource):
    def post(self):
        record = json.loads(request.data)
        try:
            user = User.objects(email=record["email"]).first()
            if user.email and bcrypt.check_password_hash(
                user.password, record["password"]
            ):
                gen_token = create_access_token(identity=user.email)
                return jsonify({"Access_Token": gen_token}, 200)
            else:
                return jsonify({"Msg": "There was error while generating token"}, 288)
        except Exception:
            return jsonify({"Msg": "Error while login the user"}, 500)
