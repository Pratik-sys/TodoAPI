import json
import bleach
from flask import jsonify, request, Blueprint
from flask_restx import Resource
from API import bcrypt, Api
from API.models import User, Todo, Subtask
from API.validation import (
    validateSubtask,
    validateTodo,
    validateTodoUpdate,
    validateSubtaskUpdate,
    validateUserDetails,
)
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    current_user,
)

_users = Blueprint("users", __name__)
users = Api(_users)


@users.route("/user/register")
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
            print(ex)
            return jsonify({"Msg": "Error while adding user to the database"}, 500)


@users.route("/user/login")
class LoginUser(Resource):
    def post(self):
        record = json.loads(request.data)
        try:
            user = User.objects(email=record["email"]).first()
            print(user)
            if user.email and bcrypt.check_password_hash(
                user.password, record["password"]
            ):
                gen_token = create_access_token(identity=user.email)
                return jsonify({"Access_Token": gen_token}, 200)
            else:
                return jsonify({"Msg": "There was error while generating token"}, 288)
        except Exception:
            return jsonify({"Msg": "Error while login the user"}, 500)
