import json
import bleach
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
class ListAllTodos(Resource):
    @jwt_required()
    def get(self):
        todo = Todo.objects(user=current_user.id)
        if todo is not None:
            return jsonify(todo, 200)
        else:
            return jsonify({"Msg": "No todo availabe for this user"}, 204)
        return jsonify({"Msg": "Error while fetching the Todo's, Please try again"}, 404)


@api.route("/<string:todo_id>/subtask")
class ListAllSubtasks(Resource):
    @jwt_required()
    def get(self, todo_id: str):
        subtask = Subtask.objects(todo=todo_id)
        if subtask is not None:
            return jsonify(subtask)
        else:
            return jsonify({"Msg": "No Subtask available for this user"}, 200)
        return jsonify({"Msg": "Error while fetching the Subtask's"}, 404)


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
                theme=bleach.clean(record["theme"])
            )
            todo.save()
            return jsonify({"Msg": "Todo Added Successfully"}, 201)
        except ValueError:
            return jsonify({"Msg": "Error while adding todo to DB"}, 500)


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
                completed=record["completed"]
            )
            subtask.save()
            return jsonify({"Msg": "Subtask Added Successfully"}, 201)
        except ValueError:
            return jsonify({"Msg": "Error while addin subtask to DB"}, 500)


@api.route("/todo/<string:todo_id>/delete")
class DeleteTodoData(Resource):
    @jwt_required()
    def delete(self, todo_id: str):
        todo = Todo.objects.filter(id=todo_id, user=current_user.id).first()
        if todo is not None:
            todo.delete()
            return jsonify({"Msg": "Todo deleted successfully"}, 202)
        else:
            return jsonify({"Msg": "No Todo to delete"}, 410)


@api.route("/<string:subtask_id>/subtask/delete")
class DeleteSubtaskData(Resource):
    @jwt_required
    def delete(self, subtask_id: str):
        subtask = Subtask.objects.get_or_404(id=subtask_id)
        if subtask is not None:
            subtask.delete()
            return jsonify({"Msg": "Subtask deleted Successfully"}, 202)
        else:
            return jsonify({"Msg": "No Subtask to delete"}, 410)


@api.route("/todo/<string:todo_id>/update")
class UpdateTodoData(Resource):
    def put(self, todo_id: str):
        todo = Todo.objects.filter(id=todo_id, user=current_user.id).first()
        record = json.loads(request.data)
        if todo is not None:
            todo.modify(title=bleach.clean(record["title"]),
                        theme=bleach.clean(record["theme"]))
            return jsonify({"Msg": "Todo updated successfully"}, 200)
        else:
            return jsonify({"Msg": "Error while updating todo"}, 404)


@api.route("/<string:todo_id>/subtask/<string:subtask_id>/update")
class UpdateSubtaskData(Resource):
    @jwt_required()
    def put(self, todo_id: str, subtask_id: str):
        subtask = Subtask.objects.filter(id=subtask_id, todo=todo_id).first()
        record = json.loads(request.data)
        if subtask is not None:
            subtask.modify(taskName=bleach.clean(record["taskname"]),
                           completed=record["completed"])
            return jsonify({"Msg": "Subtak updated successfully"}, 200)
        else:
            return jsonify({"Msg": "Error while updating subtask"}, 404)


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
                email=record["email"],
                password=hashed_password
            )
            if User.objects.filter(email=user.email).values_list('email'):
                return jsonify({"Msg": "email already in use"}, 406)
            else:
                user.save()
            return jsonify({"Msg": "User added sucessfully"}, 200)
        except ValueError:
            return jsonify({"Msg": "Error while adding user to the database"}, 500)


@api.route("/user/login")
class LoginUser(Resource):
    def post(self):
        record = json.loads(request.data)
        try:
            user = User.objects(email=record["email"]).first()
            if user.email and bcrypt.check_password_hash(user.password, record["password"]):
                gen_token = create_access_token(identity=user.email)
                return jsonify({"Access_Token": gen_token}, 200)
            else:
                return jsonify({"Msg": "There was error while generating token"}, 288)
        except ValueError:
            return jsonify({"Msg": "Error while login the user"}, 500)
