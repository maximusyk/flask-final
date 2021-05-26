from functools import wraps

import jwt
from app.extensions import csrf
from app.task_api import api_bp
from app.todo.models import *
from app.users.models import *
from flask import current_app as app
from flask import jsonify, request

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return "A valid token is missing", 401

        try:
            print("\n\n")
            print("*** Token ***")
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["public_id"]).first()
        except:
            return "Token is invalid", 401

        return f(current_user, *args, **kwargs)

    return decorated_function


@api_bp.route("/tasks", methods=["POST"])
@token_required
@csrf.exempt
def create_task(current_user):
    if not current_user.admin:
        return "You don't have permission to delete Users.", 403
    title = request.json["title"]
    description = request.json["description"]
    priority = request.json["priority"]
    category_id = request.json["category_id"]

    new_task = Task(title=title, description=description, priority=priority, category_id=category_id)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)


@api_bp.route("/tasks", methods=["GET"])
@csrf.exempt
def get_tasks():
    all_tasks = Task.query.all()

    return tasks_schema.jsonify(all_tasks)


@api_bp.route("/tasks/<id>", methods=["GET"])
@csrf.exempt
def get_task(id):
    task = Task.query.get(id)

    return task_schema.jsonify(task)


@api_bp.route("/tasks/<id>", methods=["PUT"])
@token_required
@csrf.exempt
def update_task(current_user, id):
    if not current_user.admin:
        return "You don't have permission to delete Users.", 403
    task = Task.query.get(id)
    if not task:
        return "Task not found.", 404

    title = request.json["title"]
    description = request.json["description"]
    priority = request.json["priority"]
    category_id = request.json["category_id"]

    task.title = title
    task.description = description
    task.priority = priority
    task.category_id = category_id

    db.session.commit()

    return task_schema.jsonify(task)


@api_bp.route("/tasks/<id>", methods=["DELETE"])
@token_required
@csrf.exempt
def delete_task(current_user, id):
    if not current_user.admin:
        return "You don't have permission to delete Users.", 403
    task = Task.query.get(id)
    if not task:
        return "Task not found.", 404
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)
