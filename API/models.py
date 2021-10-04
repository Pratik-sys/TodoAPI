from mongoengine.fields import ListField
from API import db, jwt
from datetime import datetime
from bson import ObjectId


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


class User(db.Document):
    name = db.StringField(required=True)
    nickname = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.utcnow)


class Subtask(db.EmbeddedDocument):
    subid = db.ObjectIdField(default=ObjectId)
    taskName = db.StringField()
    completed = db.BooleanField(default=False)
    date = db.DateTimeField(default=datetime.utcnow)


class Todo(db.Document):
    user = db.ReferenceField(User)
    title = db.StringField()
    theme = db.StringField()
    date = db.DateTimeField(default=datetime.utcnow)
    subtasks = ListField(db.EmbeddedDocumentField(Subtask))
