from flask import Blueprint
from flask.scaffold import F
from flask_restx import Api
from .Subtasks.routes import subtasks
from .Todos.routes import todos
from .Users.routes import users

blueprint = Blueprint("api", __name__, url_prefix= "/api")
api = Api(blueprint, title="Todo Api", version="1.0")

api.add_namespace(subtasks)
api.add_namespace(todos)
api.add_namespace(users)
