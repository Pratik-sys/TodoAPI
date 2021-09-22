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

todos = Namespace("todos")


@todos.route("/getAll")
class ListAllTodos(Resource):
    @jwt_required()
    def get(self):
        try:
            todo = Todo.objects(user=current_user.id).all()
            if len(todo) > 0:
                return jsonify(todo, 200)
            else:
                return jsonify({"Msg": "No todo availabe for this user"}, 204)
        except Exception as ex:
            return jsonify(
                {"Msg": "Error while fetching the Todo's, Please try again"}, 404
            )


@todos.route("/add")
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
            )
            errors = validateTodo(todo)
            if len(errors) == 0:
                todo.save()
                return jsonify({"Msg": "Todo Added Successfully"}, 201)
            else:
                return jsonify(errors, 204)
        except Exception:
            return jsonify({"Msg": "DB Error"}, 500)


@todos.route("/<string:todo_id>/update")
class UpdateTodoData(Resource):
    @jwt_required()
    def put(self, todo_id: str):
        try:
            todo = Todo.objects.filter(id=todo_id, user=current_user.id).first()
            record = json.loads(request.data)
            errors = validateTodoUpdate(record)
            if len(errors) == 0:
                todo.modify(
                    title=bleach.clean(record["title"]),
                    theme=bleach.clean(record["theme"]),
                )
                return jsonify({"Msg": "Todo updated successfully"}, 200)
            else:
                return jsonify(errors, 404)
        except Exception:
            return jsonify({"Msg": "Db Error"}, 500)


@todos.route("/<string:todo_id>/delete")
class DeleteTodoData(Resource):
    @jwt_required()
    def delete(self, todo_id: str):
        try:
            todo = Todo.objects.filter(id=todo_id, user=current_user.id).first()
            if todo is not None:
                todo.delete()
                return jsonify({"Msg": "Todo deleted successfully"}, 202)
            else:
                return jsonify({"Msg": "No Todo to delete"}, 410)
        except Exception:
            return jsonify({"Msg": "Db Error"}, 500)
