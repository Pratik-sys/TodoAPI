# TODO API

- Todo Api is implemented with [Flask](https://flask.palletsprojects.com/en/2.0.x/) Framework and  [Flask Rest-x](https://flask-restx.readthedocs.io/en/latest/index.html) for quickly building  Resful Apis.

- Authentication and Authorization of the API is done with [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)

### Technologies
---
- Flask
- Flask Rest-x
- Flask Mongoengine
- Flask-Jwt-Extended
### Run your code in local development enviroment
------
- Clone the project into your local machine

    ```bash
    $ git clone https://github.com/Pratik-sys/TodoAPI
    ```
- To run this project, install requiremnts.txt

    ```python 
    $ pip install -r requirements.txt
    ```
- Run the main file to get the server runing on your local machine
    ```python
    $ python run.py
    ```

- you can test the Api in [Postman](https://www.postman.com/) for better visualization

### View Deployment
---
> https://dynamic-todo-api.herokuapp.com/
## list of endpoints

> if you are running the server on localhost the prefix to all the endpoints will be `http://127.0.0.1:5000/`
---
## User Endpoints
```bash
api/users/register
```
```bash
api/users/login
```
---

## Todo Endpoints
```bash
api/todos/getAll
```
```bash
api/todos/add
```
```bash
api/todos/<todo_id>update
```
```bash
api/todos/<todo_id>/delete
```

-----

## Subtask Endppoints
```bash
api/subtasks/<todo_id>getAll
```
```bash
api/subtasks/<todo_id>/add
```
```bash
api/subtasks/<subtask_id>/update
```
```bash
api/subtasks/<subtask_id>/delete
```

> `Note` :- The swagger is been disabled intentionally, you can test the API on `Postman`
