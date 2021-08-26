from flask import Flask
from flask_restx import Api
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from API.config import Config
from flask_cors import CORS


api = Api(title="Todo", version="1.0")
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
    CORS(app)
    from API.models import User

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.objects(email=identity).first()

    from API.Subtasks.routes import _subtasks
    from API.Todos.routes import _todos
    from API.Users.routes import _users

    app.register_blueprint(_subtasks)
    app.register_blueprint(_todos)
    app.register_blueprint(_users)

    return app
