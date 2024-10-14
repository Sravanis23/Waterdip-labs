## Waterdip AI Backend Assignment

## Overview
A Flask-based API server that tracks tasks. The server allows for creating, listing, retrieving, deleting, and updating tasks. Additionally, it supports bulk operations for creating and deleting tasks.

## Features
- *Create Task*: Allows users to create a new task with a title and completion status.
- *List Tasks*: Retrieves all tasks created, displaying their id, title, and completion status.
- *Get Specific Task*: Fetches details of a task by its id.
- *Delete Task*: Deletes a specified task by its id.
- *Edit Task*: Updates the title or completion status of a specific task.
- *Bulk Add Tasks (Extra Credit)*: Adds multiple tasks in one request.
- *Bulk Delete Tasks (Extra Credit)*: Deletes multiple tasks in one request.

## Setup Instructions

1. Clone the repository:
   terminal
   git clone https://github.com/Sravanis23/Waterdip-labs.git (directory : /backend )
   

2. Set up the virtual environment:
   terminal
   python -m venv venv
   source venv/bin/activate
   

3. Install dependencies:
   terminal
   pip install flask flask_sqlalchemy pydantic typing flask_pydantic

   
5. Run the app:
   terminal
   ```python main.py```
   

## API Endpoints

### 1. Create a Task
*POST /v1/tasks*
- Input: ```{"title": "Test Task", "is_completed": false}```
- Output: ```{"id": 1}``` (returns a 201 status code)
   
### 2. List All Tasks
*GET /v1/tasks*
- Input: None
- Output: <br/>
```{"tasks": [{"id": 1, "title": "Test Task", "is_completed": false}]}``` <br/>
(returns a 200 status code)
   
### 3. Get a Specific Task
*GET /v1/tasks/{id}*
- Input: Task id (via URL)
- Output: ```{"id": 1, "title": "Test Task", "is_completed": false} (returns a 200 status code)```

### 4. Delete a Task
*DELETE /v1/tasks/{id}*
- Input: Task id (via URL)
- Output: None (returns a 204 status code)

### 5. Edit a Task
*PUT /v1/tasks/{id}*
- Input: ```{"title": "Updated Task", "is_completed": true}```
- Output: None (returns a 204 status code)

### 6. Bulk Add Tasks (Extra Credit)
*POST /v1/tasks/bulk*
- Input: ```{"tasks": [{"title": "Task 1", "is_completed": false}, ...]}```
- Output: ```{"tasks": [{"id": 1}, {"id": 2}, ...]} (returns a 201 status code)```

### 7. Bulk Delete Tasks (Extra Credit)
*DELETE /v1/tasks/bulk*
- Input: ```{"tasks": [1, 2, 3]}```
- Output: None (returns a 204 status code)

## Database Setup
- *SQLAlchemy* is used to define models and handle database interactions.
- *SQLite* is used for simplicity, but can be swapped for PostgreSQL for production environments.

## Task Model
- id: Integer (Primary Key)
- title: String (Required)
- is_completed: Boolean (Default: False)

## Extra Credit
- *Pydantic Schemas*: Pydantic can be used to validate input data, ensuring the structure of data is correct before database insertion.
