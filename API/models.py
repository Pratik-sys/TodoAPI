from API import db
from bson.objectid import ObjectId


class User(db.Document):
    name = db.StringField()
    nickname = db.StringField()
    email = db.StringField()
    password = db.StringField()
    date = db.DateTimeField()


class Todo(db.Document):
    user = db.ReferenceField(User)
    title = db.StringField()
    theme = db.StringField()
    date = db.DateTimeField()


class Subtask(db.Document):
    todo = db.ReferenceField(Todo)
    taskName = db.StringField()
    completed = db.BooleanField(default = False)
    date = db.DateTimeField()
