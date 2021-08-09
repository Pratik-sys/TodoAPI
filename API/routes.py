import json
from datetime import date as D
from flask import jsonify, request
from flask_restx import Resource
from API import api
from API.models import User, Todo, Subtask

@api.route("/list")
class GetData(Resource):
    def get(self):
        id = request.json.get("id")
        data = User.objects(id=id)
        if data != None:
            return jsonify(data)
        else:
            return jsonify({"msg": "Data not Found"})
        return jsonify({"msg": "Error while fetching the data."}, 404)


@api.route("/add")
class AddData(Resource):
    def post(self):
        record = json.loads(request.data)
        try:
            user = User(
                name=record["name"],
                nickname=record["nickname"],
                email=record["email"],
                password=record["password"],
                date=D.today(),
            )
            user.todos = [
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
            user.save()
            return jsonify({"msg": "data added"})
        except ValueError:
            return jsonify({"msg": "error"})


@api.route("/del")
class Deldata(Resource):
    def delete(self):
        id = request.json.get("id")
        data = User.objects(id=id)
        if data == id:
            data.delete()
            return jsonify({"msg" : "user deleted" })
        else:
            return jsonify({"msg": "no such user found"})

@api.route("/update")
class UpdateData(Resource):
    def put(self):
        record = json.loads(request.data)
        user = User.objects(name = record["name"]).first()
        if not user:
            return jsonify({"msg" : "No user found"})
        else:
            user.update(nickname = record["nickname"], email = record["email"])
            return jsonify({"msg" : "user updated"})
