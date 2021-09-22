from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from API.config import Config
from flask_cors import CORS


bcrypt = Bcrypt()
jwt = JWTManager()
db = MongoEngine()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)
    from API.models import User

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.objects(email=identity).first()

    from .test import blueprint as api

    app.register_blueprint(api)

    return app
