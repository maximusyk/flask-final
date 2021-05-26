from app.api_rest import api_rest_bp
from app.extensions import csrf
from app.todo.models import *
from flask import jsonify, request
from flask_restful import Api, Resource, fields, reqparse

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

api = Api(api_rest_bp)
resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "created": fields.String,
    "priority": fields.String,
    "is_done": fields.Boolean,
}

create_args = reqparse.RequestParser()
create_args.add_argument("title", type=str, help="Title of the Task")
create_args.add_argument("description", type=str, help="Description of the Task")
create_args.add_argument("priority", type=str, help="Priority of the Task")
create_args.add_argument("category_id", type=str, help="CategoryID of the Task")


update_args = reqparse.RequestParser()
update_args.add_argument("title", type=str, help="Title of the Task", required=True)
update_args.add_argument("description", type=str, help="Description of the Task", required=True)
update_args.add_argument("priority", type=str, help="Priority of the Task", required=True)
update_args.add_argument("category_id", type=str, help="CategoryID of the Task", required=True)


class TaskItem(Resource):
    def post(self):
        args = create_args.parse_args()
        new_task = Task(
            title=args["title"],
            description=args["description"],
            priority=args["priority"],
            category_id=args["category_id"],
        )
        db.session.add(new_task)
        db.session.commit()

        return task_schema.jsonify(new_task)

    def get(self, id=None):
        if id:
            task = Task.query.get(id)
            if not task:
                return "Task not found!", 404
            return task_schema.jsonify(task)
        else:
            all_tasks = Task.query.all()
            return tasks_schema.jsonify(all_tasks)

    def put(self, id):
        task = Task.query.get_or_404(id)
        if not task:
            return "Task not found!", 404

        args = update_args.parse_args()

        task.title = args["title"]
        task.description = args["description"]
        task.priority = args["priority"]
        task.category_id = args["category_id"]

        db.session.commit()

        return task_schema.jsonify(task)

    def delete(self, id):
        task = Task.query.get(id)
        if not task:
            return "Task not found!", 404
        db.session.delete(task)
        db.session.commit()

        return task_schema.jsonify(task)


# @api_bp.route("/tasks", methods=["POST"])
# @csrf.exempt
# def create_task():
#     title = request.json["title"]
#     description = request.json["description"]
#     priority = request.json["priority"]
#     category_id = request.json["category_id"]

#     new_task = Task(title=title, description=description, priority=priority, category_id=category_id)

#     db.session.add(new_task)
#     db.session.commit()

#     return task_schema.jsonify(new_task)


# @api_bp.route("/tasks", methods=["GET"])
# @csrf.exempt
# def get_tasks():
#     all_tasks = Task.query.all()

#     return tasks_schema.jsonify(all_tasks)


# @api_bp.route("/tasks/<id>", methods=["GET"])
# @csrf.exempt
# def get_task(id):
#     task = Task.query.get(id)

#     return task_schema.jsonify(task)


# @api_bp.route("/tasks/<id>", methods=["PUT"])
# @csrf.exempt
# def update_task(id):
#     task = Task.query.get(id)

#     title = request.json["title"]
#     description = request.json["description"]
#     priority = request.json["priority"]
#     category_id = request.json["category_id"]

#     task.title = title
#     task.description = description
#     task.priority = priority
#     task.category_id = category_id

#     db.session.commit()

#     return task_schema.jsonify(task)


# @api_bp.route("/tasks/<id>", methods=["DELETE"])
# @csrf.exempt
# def delete_product(id):
#     task = Task.query.get(id)
#     db.session.delete(task)
#     db.session.commit()

#     return task_schema.jsonify(task)


api.add_resource(TaskItem, "/tasks", "/tasks/<id>")
