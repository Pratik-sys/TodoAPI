import json
from datetime import date as D
from flask import jsonify, request
from flask_restx import Resource
from API import api
from API.models import User, Todo, Subtask


@api.route("/<string:user_id>/todos")
class GetAll(Resource):
    def get(self, user_id: str):
        data = User.objects.get_or_404(id=user_id)
        if data != None:
            return jsonify(data)
        else:
            return jsonify({"msg": "Data not Found"})
        return jsonify({"msg": "Error while fetching the data."}, 404)

@api.route("/<string:user_id>/todo/add")
class AddTodoData(Resource):
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

@api.route("/<string:user_id>/todo/delete")
class DeleteData(Resource):
    def delete(self, user_id: str):
        data = User.objects.get_or_404(id=user_id)
        if data == id:
            data.delete()
            return jsonify({"msg": "user deleted"})
        else:
            return jsonify({"msg": "no such user found"})


@api.route("/<string:user_id>/todo/<string:todo_id>/update")
class UpdateTodoData(Resource):
    def put(self, user_id: str, todo_id: str):
        data = Todo.objects.filter(id =todo_id, user = user_id).first()
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
        data = Subtask.objects.filter(id =subtask_id, todo = todo_id).first()
        print(data)
        record = json.loads(request.data)
        if data and data == None:
            return jsonify({"msg": "No subtask found"})
        else:
            data.modify(taskName=record["taskname"], completed=record["completed"])
            return jsonify({"msg": "subtask  updated"})
@api.route("/user/register")
class RegisterUser(Resource):
    def post(self):
        record = json.loads(request.data)
        try:
            user = User(
                name=record["name"],
                nickname=record["nickname"],
                email=record["email"],
                password=record["password"],
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
            print(user.password)
            if record["password"] == user.password and record["email"] == user.email:
                return jsonify({"msg": "User logged in sucessfully"})
            else:
                return jsonify({"msg": "No Such user found"})
        except ValueError:
            return jsonify({"msg": "error"})