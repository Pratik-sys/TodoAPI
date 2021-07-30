from API import db

class Subtask(db.EmbeddedDocument):
    sid = db.ObjectIdField(default=ObjectId)
    taskName = db.StringField()
    completed = db.BooleanField()
    date = db.DateTimeField()

class Todo(db.EmbeddedDocument):
    tid = db.ObjectIdField(default=ObjectId)
    title = db.StringField()
    subtasks = db.ListField(db.EmbeddedDocumentField(Subtask))
    theme = db.StringField()
    date = db.DateTimeField()

class User(db.Document):
    name = db.StringField()
    nickname = db.StringField()
    email = db.StringField()
    password = db.StringField()
    date = db.DateTimeField()
    todos = db.ListField(db.EmbeddedDocumentField(Todo))