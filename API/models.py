from API import db


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
    todo = db.ReferenceField(Todo, reverse_delete_rule=db.CASCADE)
    taskName = db.StringField()
    completed = db.BooleanField(default = False)
    date = db.DateTimeField()
