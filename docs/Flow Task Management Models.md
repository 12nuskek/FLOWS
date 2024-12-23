
# Flow Task Management Models

This document provides an overview of the SQLAlchemy models used by the **Flow Task Management** application. These models map directly to the database tables defined in the system’s schema. Developers can use this reference to understand relationships, column definitions, and how to interact with the data layer.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Key Models](#key-models)
    - [Roles, Permissions, RolePermission](#roles-permissions-rolepermission)
    - [Departments, Wards](#departments-wards)
    - [JobTypes, BreakTypes](#jobtypes-breaktypes)
    - [Users, UserProfiles](#users-userprofiles)
    - [Tasks & Related Tables](#tasks--related-tables)
    - [Feedback, Messages, Notifications](#feedback-messages-notifications)
    - [Auditing & Reporting](#auditing--reporting)
    - [Staff Management](#staff-management)
    - [Public Links](#public-links)
    - [Task Escalations](#task-escalations)
    - [System Settings](#system-settings)
    - [Incidents](#incidents)
    - [Vehicles](#vehicles)
4. [Relationships](#relationships)
5. [Usage Example](#usage-example)
6. [Further Reading](#further-reading)

---

## Introduction

These models define all database interactions for the **Flow Task Management** application. They capture roles, user accounts, tasks, feedback, vehicle assignments, and more. Each model corresponds to a single table in the underlying database (e.g., SQLite, PostgreSQL, MySQL, etc.), with relationships declared to simplify retrieving linked data.

**Key points**:
- We use [SQLAlchemy](https://docs.sqlalchemy.org/) with Flask (commonly via [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)).
- The naming of tables aligns with the initial SQL schema.
- Auto-increment primary keys are used for most tables.
- Timestamps default to `CURRENT_TIMESTAMP` (or `datetime.utcnow` in Python).
- Relationship fields are used to simplify joins (e.g., `User.tasks`, `Task.attachments`).

---

## Project Structure

Below is a typical Flask project layout which includes a `models.py` file:

```
├── app/
│   ├── __init__.py         # Initializes Flask app, config, DB, etc.
│   ├── models.py           # All SQLAlchemy models
│   ├── routes.py           # Flask routes/views
│   ├── api/                # RESTful API endpoints
│   ├── forms.py            # WTForms or similar
│   ├── static/             # CSS, JS, images
│   └── templates/          # Jinja2 templates
├── config/
│   ├── dev_config.py
│   ├── prod_config.py
│   └── test_config.py
├── tests/
│   └── test_example.py
├── docs/
│   └── design_overview.md
├── scripts/
│   └── seed_data.py
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── k8s/
│       ├── deployment.yaml
│       └── service.yaml
├── migrations/
├── .env
├── .dockerignore
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

The **`models.py`** file (or files, if you split them by domain) contains all the ORM models described in this documentation.

---

## Key Models

### Roles, Permissions, RolePermission

- **Role**: Represents different user roles (e.g., Operator, Porter, Admin).
- **Permission**: Represents granular actions or privileges in the system.
- **RolePermission**: Maps which permissions are granted to which role.

### Departments, Wards

- **Department**: High-level organizational unit (e.g., Cardiology, Radiology).
- **Ward**: Sub-unit or ward within a department.

### JobTypes, BreakTypes

- **JobType**: Defines the type of task (e.g., “Patient Transfer,” “Equipment Delivery”).  
- **BreakType**: Defines reasons or types of breaks (e.g., lunch, short rest).

### Users, UserProfiles

- **User**: Authentication and authorization entity; can be Submitters (e.g., Doctors/Nurses), Porters, Operators, or Admins.
- **UserProfile**: Supplementary data such as first name, last name, address, and alternative contact.

### Tasks & Related Tables

- **Task**: Core model for a requested job. Tracks priority, start/end time, and references to submitter/receiver.
- **PriorityChange**: Logs when a task’s priority changes.
- **TaskStatusUpdate**: Logs each status change (e.g., from “Pending” to “In Progress”).
- **TaskAttachment**: Contains file attachments (images, PDFs) linked to a task.

### Feedback, Messages, Notifications

- **Feedback**: Capture user ratings (1–5) and comments on a completed task.
- **Message**: In-app direct communication between users (e.g., staff <-> operator).
- **Notification**: System-triggered messages (e.g., “Your task is assigned!”).

### Auditing & Reporting

- **AuditLog**: Historical record of key user actions and system events, capturing old/new values.
- **Report**: Defines generated reports (e.g., CSV/PDF) and who created them.

### Staff Management

- **StaffAvailability**: Tracks porter status (“On Duty,” “Off Duty,” “On Break”), including break approvals.
- **Shift**: Tracks shift durations for each user.

### Public Links

- **PublicLink**: Allows certain stations or forms to be accessed without login (e.g., public task submission portal).

### Task Escalations

- **Escalation**: Raises a task to higher-level attention (with a reason) if it’s urgent or not progressing.

### System Settings

- **SystemSetting**: Key-value store for global or environment-specific settings (e.g., default priority, display flags).

### Incidents

- **Incident**: Reports special situations or incidents related to a task (e.g., an accident or equipment malfunction).

### Vehicles

- **Vehicle**: Tracks mobile assets like vans, carts, or ambulances, including assignment to a user and maintenance status.

---

## Relationships

Below is a high-level diagram of some major relationships:

```
Role --< RolePermission >-- Permission

Department --< Ward
Department --< User
Ward --< Task
User --< Task (submitter_id / receiver_id)
Task --< PriorityChange
Task --< TaskStatusUpdate
Task --< TaskAttachment
Task --< Feedback

User --< Message (sender_id / receiver_id)
User --< Notification
User --< StaffAvailability
User --< Shift
User --< PublicLink
User --< Escalation
User --< Incident
User --< Vehicle (assigned_to)
...
```

- **One-to-many**: e.g., a **Department** can have many **Wards** (`department_id` foreign key).
- **Many-to-many**: e.g., **Role** and **Permission** via **RolePermission**.
- **One-to-one**: e.g., **User** to **UserProfile**.

---

## Usage Example

**Initialization in `app/__init__.py`:**

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db

def create_app():
    app = Flask(__name__)
    
    # Example config; adjust as needed
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Create tables if not existing
        
    return app
```

**Creating and Querying a Task:**

```python
from app.models import db, Task, User

def create_task():
    # Assume we already have a user in the database with user_id=1
    submitter = User.query.get(1)
    
    new_task = Task(
        submitter_id=submitter.user_id,
        pick_up_location='Ward A',
        drop_off_location='Lab',
        priority='Urgent',
        patient_item_details='Blood samples',
        additional_instructions='Handle with care'
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return new_task

def get_tasks_for_user(user_id):
    tasks = Task.query.filter_by(submitter_id=user_id).all()
    return tasks
```

**Example of Updating a Task’s Status:**

```python
from app.models import db, TaskStatusUpdate

def update_task_status(task, new_status, user):
    status_update = TaskStatusUpdate(
        task_id=task.task_id,
        updated_by=user.user_id,
        status=new_status,
        comments=f'Status changed to {new_status}'
    )
    
    db.session.add(status_update)
    task.status = new_status
    db.session.commit()
```

---

## Further Reading

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/14/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Alembic/Flask-Migrate](https://alembic.sqlalchemy.org/) for database migrations.
- [PEP 8 Python Style Guide](https://peps.python.org/pep-0008/) for code formatting best practices.

---

**Author**: Flow Task Management Team  
**Version**: 1.0.0  
**Last Updated**: *\[Date\]*  

---

> **Tip:** Clone this repo, install dependencies (`pip install -r requirements.txt`), and run `flask run` (or `python run.py`) to start the application in development mode.
