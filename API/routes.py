import json
import bleach
from datetime import date as D
from flask import jsonify, request
from flask_restx import Resource
from API import api, bcrypt, jwt
from API.models import User, Todo, Subtask
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, current_user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.objects(email=identity).first()


@api.route("/todos")
class GetAll(Resource):
    @jwt_required()
    def get(self):
        data = Todo.objects(user=current_user.id)
        if data is not None:
            return jsonify(data)
        else:
            return jsonify({"msg": "Data not Found"})
        return jsonify({"msg": "Error while fetching the data."}, 404)


@api.route("/todo/add")
class AddTodoData(Resource):
    @jwt_required()
    def post(self):
        record = json.loads(request.data)
        try:
            user = User.objects.get(id=current_user.id)
            todo = Todo(
                user=user,
                title=bleach.clean(record["title"]),
                theme=bleach.clean(record["theme"]),
                date=D.today()
            )
            todo.save()
            return jsonify({"msg": "data added"})
        except ValueError:
            return jsonify({"msg": "error"})


@api.route("/<string:todo_id>/subtask/add")
class AddSubtaskData(Resource):
    @jwt_required()
    def post(self, todo_id: str):
        record = json.loads(request.data)
        try:
            todo = Todo.objects.get(id=todo_id)
            subtask = Subtask(
                todo=todo,
                taskName=bleach.clean(record["taskname"]),
                completed=record["completed"],
                date=D.today()
            )
            subtask.save()
            return jsonify({"msg": "data added"})
        except ValueError:
            return jsonify({"msg": "error"})


@api.route("/todo/<string:todo_id>/delete")
class DeleteTodoData(Resource):
    @jwt_required()
    def delete(self, todo_id: str):
        data = Todo.objects.filter(id=todo_id, user=current_user.id).first()
        data.delete()
        return jsonify({"msg": "deleted"})


@api.route("/<string:subtask_id>/subtask/delete")
class DeleteSubtaskData(Resource):
    @jwt_required
    def delete(self, subtask_id: str):
        data = Subtask.objects.get_or_404(id=subtask_id)
        if data != None:
            data.delete()
            return jsonify({"msg": "Subtask deleted"})
        else:
            return jsonify({"msg": "Error, no such subtask found in database"})


@api.route("/todo/<string:todo_id>/update")
class UpdateTodoData(Resource):
    def put(self, todo_id: str):
        data = Todo.objects.filter(id=todo_id, user=current_user.id).first()
        print(data)
        record = json.loads(request.data)
        if data and data == None:
            return jsonify({"msg": "No todo found"})
        else:
            data.modify(title=bleach.clean(record["title"]),
                        theme=bleach.clean(record["theme"]))
            return jsonify({"msg": "todo updated"})


@api.route("/<string:todo_id>/subtask/<string:subtask_id>/update")
class UpdateSubtaskData(Resource):
    @jwt_required()
    def put(self, todo_id: str, subtask_id: str):
        data = Subtask.objects.filter(id=subtask_id, todo=todo_id).first()
        print(data)
        record = json.loads(request.data)
        if data and data == None:
            return jsonify({"msg": "No subtask found"})
        else:
            data.modify(taskName=bleach.clean(record["taskname"]),
                        completed=record["completed"])
            return jsonify({"msg": "subtask  updated"})


@api.route("/user/register")
class RegisterUser(Resource):
    def post(self):
        record = json.loads(request.data)
        try:
            hashed_password = bcrypt.generate_password_hash(
                bleach.clean(record["password"])).decode('utf-8')
            user = User(
                name=bleach.clean(record["name"]),
                nickname=bleach.clean(record["nickname"]),
                email=bleach.clear(record["email"]),
                password=hashed_password,
                date=D.today()
            )
            if User.objects.filter(email=user.email).values_list('email'):
                return jsonify({"msg": "email already in use"})
            else:
                user.save()
            return jsonify({"msg": "User added sucessfully"})
        except ValueError:
            return jsonify({"msg": "Failed adding user"})


@api.route("/user/login")
class LoginUser(Resource):
    def post(self):
        record = json.loads(request.data)
        try:
            user = User.objects(email=record["email"]).first()
            if user.email and bcrypt.check_password_hash(user.password, record["password"]):
                gen_token = create_access_token(identity=user.email)
                return jsonify({"access_token": gen_token})
            else:
                return jsonify({"msg": "No Such user found"})
        except ValueError:
            return jsonify({"msg": "error"})
