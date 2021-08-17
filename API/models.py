from API import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


class User(UserMixin, db.Document):
    name = db.StringField()
    nickname = db.StringField()
    email = db.StringField()
    password = db.StringField()
    date = db.DateTimeField()


class Todo(UserMixin, db.Document):
    user = db.ReferenceField(User)
    title = db.StringField()
    theme = db.StringField()
    date = db.DateTimeField()


class Subtask(UserMixin, db.Document):
    todo = db.ReferenceField(Todo, reverse_delete_rule=db.CASCADE)
    taskName = db.StringField()
    completed = db.BooleanField(default=False)
    date = db.DateTimeField()
