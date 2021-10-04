import json
import bleach
from flask import jsonify, request
from flask_restx import Resource, Namespace
from API.models import Todo, Subtask
from API.validation import validateSubtask, validateSubtaskUpdate
from flask_jwt_extended import jwt_required

subtasks = Namespace("subtasks")


@subtasks.route("/<string:todo_id>/getAll")
class ListAllSubtasks(Resource):
    @jwt_required()
    def get(self, todo_id: str):
        try:
            todosub = Todo.objects(id=todo_id).first()
            if len(todosub.subtasks) > 0:
                return jsonify(todosub.subtasks)
            else:
                return jsonify({"Msg": "No Subtask available for this user"}, 200)
        except Exception as ex:
            return jsonify({"Msg": "Error while fetching the Subtask's"}, 404)


@subtasks.route("/<string:todo_id>/add")
class AddSubtaskData(Resource):
    @jwt_required()
    def post(self, todo_id: str):
        record = json.loads(request.data)
        subarr = []
        try:
            errors = validateSubtask(record)
            if len(errors) == 0:
                todosub = Todo.objects(id=todo_id).first()
                if len(todosub.subtasks) == 0:
                    subarr = [
                        Subtask(
                            taskName=bleach.clean(record["taskname"]),
                            completed=record["completed"],
                        )
                    ]
                else:
                    subarr = todosub.subtasks
                    subarr.append(
                        Subtask(
                            taskName=bleach.clean(record["taskname"]),
                            completed=record["completed"],
                        )
                    )
                todosub.subtasks = subarr
                todosub.save()
                return jsonify({"Msg": "Subtask Added Successfully"}, 201)
            else:
                return jsonify(errors, 204)
        except Exception as ex:
            print(ex)
            return jsonify({"Msg": "DB Error"}, 500)


@subtasks.route("/<string:subtask_id>/update")
class UpdateSubtaskData(Resource):
    @jwt_required()
    def put(self, subtask_id: str):
        record = json.loads(request.data)
        try:
            errors = validateSubtaskUpdate(record)
            todosub = Todo.objects(subtasks__subid=subtask_id).first()
            if len(errors) == 0:
                for i in todosub.subtasks:
                    if str(i.subid) == subtask_id:
                        i.taskName = bleach.clean(record["taskname"])
                        i.completed = i.completed or record["completed"]
                todosub.save()
                return jsonify({"Msg": "Subtak updated successfully"}, 200)
            else:
                return jsonify(errors, 204)
        except Exception as ex:
            print(ex)
            return jsonify({"Msg": "DB Error"}, 500)


@subtasks.route("/<string:subtask_id>/delete")
class DeleteSubtaskData(Resource):
    @jwt_required()
    def delete(self, subtask_id: str):
        subarr = []
        try:
            todosub = Todo.objects(subtasks__subid=subtask_id).first()
            for i in todosub.subtasks:
                if str(i.subid) != subtask_id:
                    subarr.append(i)
            todosub.subtasks = subarr
            todosub.save()
            return jsonify({"Msg": "Subtask deleted Successfully"}, 202)
        except Exception as ex:
            return jsonify({"Msg": "Db Error"}, 500)
