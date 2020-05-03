from .app import app, auth
from flask import jsonify, make_response, request, abort, url_for


PATH = "/api/todo/v0.1"


tasks = [
    {
        "id": 1,
        "title": "Buy Groceries",
        "description": "Milk, Cheese, Fruit",
        "done": False
    },
    {
        "id": 2,
        "title": "Learn Python",
        "description": "Find a well structured tutorial",
        "done": False
    }
]


@auth.get_password
def get_password(user):
    if user == "hamza":
        return "123"
    return None


@auth.error_handler
def unauthorized():
    return jsonify({"error": "Unauthorized access"}), 403


@app.route("/")
@app.route("/index")
@app.route(PATH)
def index():
    return "<h1>Todo App</h1>"


@app.route(f"{PATH}/tasks")
@auth.login_required
def get_tasks():
    return jsonify({"tasks": [task_uri(t) for t in tasks]}), 200


@app.route(f"{PATH}/tasks/<int:task_id>")
def get_task(task_id):
    task = [t for t in tasks if t["id"] == task_id]

    if len(task) == 0:
        return make_response("Resource not found!", 404)

    return jsonify({"task": task_uri(task[0])}), 200


@app.route(f"{PATH}/tasks", methods=["POST"])
def create_task():
    if not request.json or "title" not in request.json:
        make_response("Invalid task syntax", 400)

    task = {
        "id": tasks[-1]["id"] + 1,
        "title": request.json["title"],
        "description": request.json.get("description", ""),
        "done": False
    }

    tasks.append(task)

    return jsonify({"task": task_uri(task)}), 201


@app.route(f"{PATH}/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if not request.json:
        return abort(400)

    task = [t for t in tasks if t["id"] == task_id]

    if len(task) == 0:
        return make_response("Resource not found!", 404)

    task = task[0]

    if "title" in request.json:
        title = request.json["title"].strip()
        if type(title) is not str or not title:
            return make_response("Task title must be of string type and cannot be empty", 400)

        task["title"] = title

    if "description" in request.json:
        description = request.json["description"].strip()
        if type(description) is not str:
            return make_response("Task description must be of string type", 400)

        task["description"] = request.json.get("description")

    if "done" in request.json:
        status = request.json["done"]
        if type(status) is not bool:
            return make_response("Task status must be of boolean type", 400)

        task["done"] = status

    return jsonify({"task": task_uri(task)}), 200


@app.route(f"{PATH}/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = [t for t in tasks if t["id"] == task_id]

    if len(task) == 0:
        return make_response("Resource not found!", 404)

    tasks.remove(task[0])

    return jsonify({"result": True}), 200


def task_uri(task):
    _task = {}
    for field in task:
        _task[field] = task[field]

        if field == "id":
            _task[field] = url_for("get_task", task_id=task[field], _external=True)

    return _task
