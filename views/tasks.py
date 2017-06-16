from flask import Blueprint, request, jsonify
from tools.auth import authorize
from models.task import Task
from database import db


tasks = Blueprint("tasks", __name__)


@tasks.route("/tasks", methods=["POST", "GET"])
@authorize
def add_or_list(user):
    if request.method == "POST":
        task = Task(**request.get_json(), user=user)
        db.session.add(task)
        db.session.commit()

        return jsonify(task=task.for_task), 200
    else:
        tasks = Task.query.filter_by(user_id=user.id).all()
        list_of_tasks = [task.for_task for task in tasks]

        return jsonify(tasks=list_of_tasks), 200


@tasks.route("/tasks/<int:task_id>", methods=["PUT", "DELETE"])
@authorize
def delete_task(user, task_id):
    task = Task.query.get(task_id)
    if not task:
        return "Task doesn\'t exist", 400

    if task.user_id != user.id:
        return "You don\'t own this task!", 401

    if request.method == "PUT":
        new_body = request.get_json()
        if task.body != new_body["body"]:
            task['body'] = new_body["body"]
            db.session.commit()

        return jsonify(task=task.for_task), 200

    else:
        db.session.delete(task)
        db.session.commit()
        return jsonify(Status="OK"), 200
