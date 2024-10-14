from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, ValidationError, Field
from typing import List, Optional
from flask_pydantic import validate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task model for database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Pydantic model for validation
class TaskModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    is_completed: Optional[bool] = False

class BulkTaskModel(BaseModel):
    tasks: List[TaskModel]

class BulkDeleteModel(BaseModel):
    tasks: List[int]

# Helper function to convert task object to dictionary
def task_to_dict(task):
    return {"id": task.id, "title": task.title, "is_completed": task.is_completed}

@app.route('/', methods=['GET'])
def default_route():
    return "App is working", 200

# Create a new task with Pydantic validation
@app.route('/v1/tasks', methods=['POST'])
@validate()  # Validate using Pydantic
def create_task(body: TaskModel):
    new_task = Task(title=body.title, is_completed=body.is_completed)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id}), 201

# List all tasks
@app.route('/v1/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    return jsonify({"tasks": [task_to_dict(task) for task in tasks]}), 200

# Get a specific task
@app.route('/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404, description="There is no task at that id")
    return jsonify(task_to_dict(task)), 200

# Delete a specific task
@app.route('/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return '', 204

# Edit a task (update) with Pydantic validation
@app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
@validate()
def update_task(task_id, body: TaskModel):
    task = Task.query.get(task_id)
    if not task:
        abort(404, description="There is no task at that id")

    task.title = body.title
    task.is_completed = body.is_completed
    db.session.commit()
    return '', 204

# Bulk add tasks with Pydantic validation
@app.route('/v1/tasks/bulk', methods=['POST'])
@validate()
def bulk_create_tasks(body: BulkTaskModel):
    tasks_to_add = [Task(title=task.title, is_completed=task.is_completed) for task in body.tasks]
    db.session.add_all(tasks_to_add)
    db.session.commit()

    return jsonify({"tasks": [{"id": task.id} for task in tasks_to_add]}), 201

# Bulk delete tasks with Pydantic validation
@app.route('/v1/tasks/bulk', methods=['DELETE'])
@validate()
def bulk_delete_tasks(body: BulkDeleteModel):
    Task.query.filter(Task.id.in_(body.tasks)).delete(synchronize_session=False)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
