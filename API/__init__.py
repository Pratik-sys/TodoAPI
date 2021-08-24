from flask import Flask
from flask_restx import Api
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from API.config import Config


api = Api()
bcrypt = Bcrypt()
jwt = JWTManager()
db = MongoEngine()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    from API.Subtasks.routes import _subtasks
    from API.Todos.routes import _todos
    from API.Users.routes import _users
    app.register_blueprint(_subtasks)
    app.register_blueprint(_todos)
    app.register_blueprint(_users)

    return app