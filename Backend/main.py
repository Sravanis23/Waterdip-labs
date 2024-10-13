from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Helper function to convert task object to dictionary
def task_to_dict(task):
    return {"id": task.id, "title": task.title, "is_completed": task.is_completed}


# Create a new task
@app.route('/', methods=['GET'])
def default_route():
    return "App is working", 200
@app.route('/v1/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if 'title' not in data:
        abort(400, description="Title is required")
    new_task = Task(title=data['title'], is_completed=data.get('is_completed', False))
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

# Edit a task (update)
@app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404, description="There is no task at that id")

    data = request.get_json()
    if 'title' in data:
        task.title = data['title']
    if 'is_completed' in data:
        task.is_completed = data['is_completed']

    db.session.commit()
    return '', 204

# Bulk add tasks (extra credit)
@app.route('/v1/tasks/bulk', methods=['POST'])
def bulk_create_tasks():
    data = request.get_json()
    if 'tasks' not in data or not isinstance(data['tasks'], list):
        abort(400, description="Tasks must be provided as a list")
    
    tasks_to_add = []
    for task_data in data['tasks']:
        if 'title' not in task_data:
            abort(400, description="Each task must have a title")
        task = Task(title=task_data['title'], is_completed=task_data.get('is_completed', False))
        tasks_to_add.append(task)
    
    db.session.add_all(tasks_to_add)
    db.session.commit()

    return jsonify({"tasks": [{"id": task.id} for task in tasks_to_add]}), 201

# Bulk delete tasks (extra credit)
@app.route('/v1/tasks/bulk', methods=['DELETE'])
def bulk_delete_tasks():
    data = request.get_json()
    if 'tasks' not in data or not isinstance(data['tasks'], list):
        abort(400, description="Tasks must be provided as a list of ids")

    Task.query.filter(Task.id.in_(data['tasks'])).delete(synchronize_session=False)
    db.session.commit()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
