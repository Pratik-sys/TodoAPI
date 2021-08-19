from API import db,jwt
import datetime


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

class User(db.Document):
    name = db.StringField(required=True)
    nickname = db.StringField(required=True,min_length=3, max_length=10)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=8,max_length=18)
    date = db.DateTimeField(default=datetime.datetime.utcnow)


class Todo(db.Document):
    user = db.ReferenceField(User)
    title = db.StringField()
    theme = db.StringField()
    date = db.DateTimeField()


class Subtask(db.Document):
    todo = db.ReferenceField(Todo, reverse_delete_rule=db.CASCADE)
    taskName = db.StringField()
    completed = db.BooleanField(default = False)
    date = db.DateTimeField()
