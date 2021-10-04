from API.models import User
import re


def validateSubtask(subtask):
    errors = []
    if subtask["taskname"] == "":
        errors.append({"Taskname": "Taskname can't be empty"})
    return errors


def validateTodo(todo):
    errors = []
    if todo.title == "":
        errors.append({"Title": "Title can't empty"})
    return errors


def validateTodoUpdate(record):
    errors = []
    if record["title"] == "":
        errors.append({"Title": "Empty Field can't be updated"})
    return errors


def validateSubtaskUpdate(record):
    errors = []
    if record["taskname"] == "":
        errors.append({"Taskname": "Empty Field can't be updated"})
    return errors


def validateUserDetails(user):
    errors = []
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if len(user.nickname) < 3:
        errors.append(
            {"Nickname": "String value is too short, should be greatere than 3"}
        )
    if User.objects.filter(email=user.email).values_list("email"):
        errors.append({"Msg": "email already in use"})

    if re.fullmatch(regex, user.email):
        pass
    else:
        errors.append({"Email": "Inavalid Email"})
    return errors
