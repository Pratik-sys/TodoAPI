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
class AddData(Resource):
    def post(self, user_id: str):
        record = json.loads(request.data)
        try:
            Todos = [
                Todo(
                    title=record["title"],
                    subtasks=[
                        Subtask(
                            taskName=record["taskname"],
                            completed=record["completed"],
                            date=D.today(),
                        )
                    ],
                    theme=record["theme"],
                    date=D.today(),
                )
            ]
            User.objects(id=user_id).update(push__todos__1 =Todos)
            return jsonify({"msg": "data added"})
        except ValueError:
            return jsonify({"msg": "error"})


@api.route("/<string:user_id>/todo/delete")
class Deldata(Resource):
    def delete(self, user_id: str):
        data = User.objects.get_or_404(id=user_id)
        if data == id:
            data.delete()
            return jsonify({"msg": "user deleted"})
        else:
            return jsonify({"msg": "no such user found"})


@api.route("/todo/update")
class UpdateData(Resource):
    def put(self):
        record = json.loads(request.data)
        user = User.objects(name=record["name"]).first()
        if not user:
            return jsonify({"msg": "No user found"})
        else:
            user.update(nickname=record["nickname"], email=record["email"])
            return jsonify({"msg": "user updated"})


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
