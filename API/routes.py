from flask import jsonify, request
from flask_restx import Resource
from API import api
from API.models import User, Todo, Subtask
from datetime import date as D
import json


@api.route("/list")
class GetData(Resource):
    def get(self):
        name = request.json.get("name")
        try:
            data = User.objects(name=name).first()
            if data != None:
                return jsonify(data)
            else:
                return jsonify({"msg": "Data not Found"})
        except:
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
        except:
            return jsonify({"msg" : "error"})