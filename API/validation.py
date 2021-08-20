def validateSubtask(subtask):
    errors = []
    if subtask.taskname == "":
        errors.append({"Taskname":"Taskname can't be empty"})
    return errors

def validateTodo(todo):
    errors = []
    if todo.title == "":
        errors.append({"Title":"Title can't empty"})
    return errors

def validateTodoUpdate(record):
    errors = []
    if record["title"] == "":
        errors.append({"Title" : "Empty Field can't be updated"})
    return errors

def validateSubtaskUpdate(record):
    errors = []
    if record["taskname"] == "":
        errors.append({"Taskname" : "Empty Field can't be updated"})
    return errors