from flask import Flask
from flask_restx import Api
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os
import random, string
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)
load_dotenv(".env")
app.config["MONGODB_SETTINGS"] = {"host": os.getenv("URI")}
db = MongoEngine(app)
app.config["SECRET_KEY"] = "".join(
    random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
    for _ in range(16)
)

bcrypt = Bcrypt(app)

app.config['JWT_SECRET_KEY'] = "".join(
    random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
    for _ in range(16)
) 

jwt = JWTManager(app)

from API import routes