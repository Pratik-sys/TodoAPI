import json
from datetime import date as D
from flask import jsonify, request
from flask_restx import Resource
from API import api, bcrypt
from API.models import User, Todo, Subtask
from flask_login import login_user, current_user, logout_user, login_required


@api.route("/<string:user_id>/todos")
class GetAll(Resource):
    @login_required
    def get(self, user_id: str):
        data = Todo.objects(user=user_id).first()        
        if data is not None:
            return jsonify(data)
        else:
            return jsonify({"msg": "Data not Found"})
        return jsonify({"msg": "Error while fetching the data."}, 404)


@api.route("/<string:user_id>/todo/add")
class AddTodoData(Resource):
    @login_required
    def post(self, user_id: str):
        record = json.loads(request.data)
        try:
            user = User.objects.get(id=user_id)
            todo = Todo(
                user=user,
                title=record["title"],
                theme=record["theme"],
                date=D.today()
            )
            todo.save()
            return jsonify({"msg": "data added"})
        except ValueError:
            return jsonify({"msg": "error"})


@api.route("/<string:todo_id>/subtask/add")
class AddSubtaskData(Resource):
    def post(self, todo_id: str):
        record = json.loads(request.data)
        try:
            todo = Todo.objects.get(id=todo_id)
            subtask = Subtask(
                todo=todo,
                taskName=record["taskname"],
                completed=record["completed"],
                date=D.today()
            )
            subtask.save()
            return jsonify({"msg": "data added"})
        except ValueError:
            return jsonify({"msg": "error"})


@api.route("/<string:user_id>/todo/<string:todo_id>/delete")
class DeleteTodoData(Resource):
    def delete(self, user_id: str, todo_id: str):
        data = Todo.objects.filter(id=todo_id, user=user_id).first()
        data.delete()
        return jsonify({"msg": "deleted"})


@api.route("/<string:subtask_id>/subtask/delete")
class DeleteSubtaskData(Resource):
    def delete(self, subtask_id: str):
        data = Subtask.objects.get_or_404(id=subtask_id)
        if data != None:
            data.delete()
            return jsonify({"msg": "Subtask deleted"})
        else:
            return jsonify({"msg": "Error, no such subtask found in database"})


@api.route("/<string:user_id>/todo/<string:todo_id>/update")
class UpdateTodoData(Resource):
    def put(self, user_id: str, todo_id: str):
        data = Todo.objects.filter(id=todo_id, user=user_id).first()
        print(data)
        record = json.loads(request.data)
        if data and data == None:
            return jsonify({"msg": "No todo found"})
        else:
            data.modify(title=record["title"], theme=record["theme"])
            return jsonify({"msg": "todo updated"})


@api.route("/<string:todo_id>/subtask/<string:subtask_id>/update")
class UpdateSubtaskData(Resource):
    def put(self, todo_id: str, subtask_id: str):
        data = Subtask.objects.filter(id=subtask_id, todo=todo_id).first()
        print(data)
        record = json.loads(request.data)
        if data and data == None:
            return jsonify({"msg": "No subtask found"})
        else:
            data.modify(taskName=record["taskname"],
                        completed=record["completed"])
            return jsonify({"msg": "subtask  updated"})


@api.route("/user/register")
class RegisterUser(Resource):
    def post(self):
        record = json.loads(request.data)
        try:
            hashed_password = bcrypt.generate_password_hash(
                record["password"]).decode('utf-8')
            user = User(
                name=record["name"],
                nickname=record["nickname"],
                email=record["email"],
                password=hashed_password,
                date=D.today()
            )
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
            if user and bcrypt.check_password_hash(user.password, record["password"]):
                login_user(user)
                return jsonify({"msg": "User logged in sucessfully"})
            else:
                return jsonify({"msg": "No Such user found"})
        except ValueError:
            return jsonify({"msg": "error"})
