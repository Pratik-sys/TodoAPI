import json
import bleach
from flask import jsonify, request, Blueprint
from flask_restx import Resource, Namespace
from API import jwt
from API.models import User, Todo, Subtask
from API.validation import (
    validateSubtask,
    validateTodo,
    validateTodoUpdate,
    validateSubtaskUpdate,
)
from flask_jwt_extended import jwt_required, create_access_token, current_user

subtasks = Namespace("subtask")


@subtasks.route("/<string:todo_id>")
class ListAllSubtasks(Resource):
    @jwt_required()
    def get(self, todo_id: str):
        try:
            subtask = Subtask.objects(todo=todo_id).all()
            if len(subtask) > 0:
                return jsonify(subtask)
            else:
                return jsonify({"Msg": "No Subtask available for this user"}, 200)
        except Exception:
            return jsonify({"Msg": "Error while fetching the Subtask's"}, 404)


@subtasks.route("/<string:todo_id>/add")
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
            )
            errors = validateSubtask(subtask)
            if len(errors) == 0:
                subtask.save()
                return jsonify({"Msg": "Subtask Added Successfully"}, 201)
            else:
                return jsonify(errors, 204)
        except Exception:
            return jsonify({"Msg": "DB Error"}, 500)


@subtasks.route("/<string:todo_id>/subtask/<string:subtask_id>/update")
class UpdateSubtaskData(Resource):
    @jwt_required()
    def put(self, todo_id: str, subtask_id: str):
        try:
            subtask = Subtask.objects.filter(id=subtask_id, todo=todo_id).first()
            record = json.loads(request.data)
            errors = validateSubtaskUpdate(record)
            if len(errors) == 0:
                subtask.modify(
                    taskName=bleach.clean(record["taskname"]),
                    completed=record["completed"],
                )
                return jsonify({"Msg": "Subtak updated successfully"}, 200)
            else:
                return jsonify(errors, 204)
        except Exception:
            return jsonify({"Msg": "DB Error"}, 500)


@subtasks.route("/<string:subtask_id>/delete")
class DeleteSubtaskData(Resource):
    @jwt_required()
    def delete(self, subtask_id: str):
        try:
            subtask = Subtask.objects.get_or_404(id=subtask_id)
            if subtask is not None:
                subtask.delete()
                return jsonify({"Msg": "Subtask deleted Successfully"}, 202)
            else:
                return jsonify({"Msg": "No Subtask to delete"}, 410)
        except Exception:
            return jsonify({"Msg": "Db Error"}, 500)
