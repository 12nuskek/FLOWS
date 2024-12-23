Flow Task Management API
========================

This document provides an overview of the RESTful API endpoints for the **Flow Task Management** application. Each endpoint is designed to interact with the underlying SQLAlchemy models (as described in `models.py`) and fulfill the user stories documented in the system.

-   **Base URL** (example): `https://api.flow-taskmanager.com/v1/`
-   **Auth Method**: Typically **JWT** or session-based auth (depending on your setup).
-   **Content-Type**: `application/json` (except for file uploads where multipart/form-data might be used).
-   **Response Format**: JSON.
-   **Error Handling**: Return HTTP error codes (4xx/5xx) and an error object:

    json

    Copy code

    `{
      "error": "Bad Request",
      "message": "Priority field is required."
    }`

* * * * *

Table of Contents
-----------------

1.  [Authentication & Authorization](#1-authentication--authorization)
2.  [User Management](#2-user-management)
3.  [Roles & Permissions](#3-roles--permissions)
4.  [Departments & Wards](#4-departments--wards)
5.  [Job Types & Break Types](#5-job-types--break-types)
6.  [Tasks](#6-tasks)
7.  [Task-Related Endpoints (Priority, Status, Attachments)](#7-task-related-endpoints-priority-status-attachments)
8.  [Feedback, Messages, Notifications](#8-feedback-messages-notifications)
9.  [Auditing & Reporting](#9-auditing--reporting)
10. [Staff Management (Availability, Shifts)](#10-staff-management-availability-shifts)
11. [Public Links](#11-public-links)
12. [Task Escalations](#12-task-escalations)
13. [System Settings](#13-system-settings)
14. [Incidents](#14-incidents)
15. [Vehicles](#15-vehicles)
16. [Versioning & Future Enhancements](#16-versioning--future-enhancements)

* * * * *

1\. Authentication & Authorization
----------------------------------

### 1.1 Login

-   **Endpoint**: `POST /auth/login`
-   **Description**: Authenticates a user (Submitter, Porter, Operator, etc.) with username/password and returns a token (JWT or session cookie).
-   **Request Body**:

    json

    Copy code

    `{
      "username": "john_doe",
      "password": "secret"
    }`

-   **Response** (success):

    json

    Copy code

    `{
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user_id": 1,
      "role": "Porter"
    }`

-   **Response** (error):

    json

    Copy code

    `{
      "error": "Unauthorized",
      "message": "Invalid username or password"
    }`

### 1.2 Logout

-   **Endpoint**: `POST /auth/logout`
-   **Description**: Invalidates the user's current session or JWT token.
-   **Response** (success):

    json

    Copy code

    `{
      "message": "Logged out successfully."
    }`

* * * * *

2\. User Management
-------------------

### 2.1 Create a User

-   **Endpoint**: `POST /users`
-   **Permissions**: Operator or Admin role typically required.
-   **Description**: Creates a new user (Porter, Operator, Submitter, etc.).
-   **Request Body**:

    json

    Copy code

    `{
      "username": "porter_jane",
      "password": "SomeStrongPass!",
      "role_id": 2,    // e.g., reference to 'Porter' role
      "department_id": 1,
      "email": "jane@example.com",
      "phone": "123-456-7890",
      "is_active": true
    }`

-   **Response** (success):

    json

    Copy code

    `{
      "user_id": 5,
      "username": "porter_jane",
      "role_id": 2,
      "department_id": 1,
      "email": "jane@example.com",
      "is_active": true,
      "created_at": "2024-01-01T12:34:56"
    }`

### 2.2 Get All Users

-   **Endpoint**: `GET /users`
-   **Description**: Retrieves a list of all users (supports filtering, e.g. `?role=porter`).
-   **Response** (success):

    json

    Copy code

    `[
      {
        "user_id": 1,
        "username": "operator_1",
        "role_id": 1,
        "is_active": true
      },
      {
        "user_id": 2,
        "username": "porter_jane",
        "role_id": 2,
        "is_active": true
      }
    ]`

### 2.3 Get Single User

-   **Endpoint**: `GET /users/{user_id}`
-   **Description**: Retrieves details about a specific user.
-   **Response** (success):

    json

    Copy code

    `{
      "user_id": 2,
      "username": "porter_jane",
      "role_id": 2,
      "department_id": 1,
      "email": "jane@example.com",
      "phone": "123-456-7890",
      "is_active": true,
      "created_at": "2024-01-01T12:34:56",
      "updated_at": "2024-01-02T10:20:00"
    }`

### 2.4 Update User

-   **Endpoint**: `PUT /users/{user_id}`
-   **Description**: Updates user information.
-   **Request Body** (example):

    json

    Copy code

    `{
      "email": "jane_porter@example.com",
      "phone": "555-555-5555",
      "is_active": false
    }`

-   **Response** (success):

    json

    Copy code

    `{
      "message": "User updated successfully.",
      "user": {
        "user_id": 2,
        "email": "jane_porter@example.com",
        "phone": "555-555-5555",
        "is_active": false
      }
    }`

### 2.5 Delete User

-   **Endpoint**: `DELETE /users/{user_id}`
-   **Description**: Deletes or deactivates a user (depending on business logic).
-   **Response** (success):

    json

    Copy code

    `{
      "message": "User deleted."
    }`

* * * * *

3\. Roles & Permissions
-----------------------

### 3.1 List Roles

-   **Endpoint**: `GET /roles`
-   **Description**: Returns a list of all roles (e.g., "Admin," "Operator," "Porter," "Submitter").
-   **Response**:

    json

    Copy code

    `[
      {
        "role_id": 1,
        "name": "Admin",
        "description": "System administrator",
        "created_at": "2024-01-01T12:00:00"
      },
      {
        "role_id": 2,
        "name": "Porter",
        "description": "Frontline staff",
        "created_at": "2024-01-01T12:05:00"
      }
    ]`

### 3.2 Create Permission

-   **Endpoint**: `POST /permissions`
-   **Description**: Creates a new permission (e.g., "CAN_VIEW_REPORTS").
-   **Request Body**:

    json

    Copy code

    `{
      "name": "CAN_VIEW_REPORTS",
      "description": "Grants ability to view detailed reports."
    }`

-   **Response** (success):

    json

    Copy code

    `{
      "permission_id": 10,
      "name": "CAN_VIEW_REPORTS",
      "description": "Grants ability to view detailed reports.",
      "created_at": "2024-01-03T09:15:00"
    }`

### 3.3 Assign Permission to Role

-   **Endpoint**: `POST /roles/{role_id}/permissions`
-   **Description**: Grants a specific permission to a role.
-   **Request Body**:

    json

    Copy code

    `{
      "permission_id": 10
    }`

-   **Response** (success):

    json

    Copy code

    `{
      "role_id": 2,
      "permission_id": 10,
      "message": "Permission assigned to role."
    }`

* * * * *

4\. Departments & Wards
-----------------------

### 4.1 Get Departments

-   **Endpoint**: `GET /departments`
-   **Description**: Lists all departments in the organization (e.g., Radiology, Cardiology).
-   **Response**:

    json

    Copy code

    `[
      {
        "department_id": 1,
        "name": "Radiology",
        "location": "Building A",
        "created_at": "2024-01-01T10:00:00"
      },
      {
        "department_id": 2,
        "name": "Cardiology",
        "location": "Building B",
        "created_at": "2024-01-02T09:00:00"
      }
    ]`

### 4.2 Get Wards by Department

-   **Endpoint**: `GET /departments/{department_id}/wards`
-   **Description**: Retrieves all wards under a specific department.
-   **Response**:

    json

    Copy code

    `[
      {
        "ward_id": 1,
        "name": "Ward A",
        "created_at": "2024-01-01T10:10:00"
      },
      {
        "ward_id": 2,
        "name": "Ward B",
        "created_at": "2024-01-01T10:15:00"
      }
    ]`

* * * * *

5\. Job Types & Break Types
---------------------------

### 5.1 List Job Types

-   **Endpoint**: `GET /job-types`
-   **Description**: Returns all defined job types (e.g., "Equipment Delivery," "Patient Transfer").
-   **Response**:

    json

    Copy code

    `[
      {
        "job_type_id": 1,
        "name": "Equipment Delivery",
        "description": "Delivery of medical equipment.",
        "is_active": true
      }
    ]`

### 5.2 Create Break Type

-   **Endpoint**: `POST /break-types`
-   **Description**: Creates a break type (e.g., "Lunch Break," "Short Rest").
-   **Request Body**:

    json

    Copy code

    `{
      "name": "Lunch Break",
      "description": "30-minute lunch break"
    }`

-   **Response** (success):

    json

    Copy code

    `{
      "break_type_id": 1,
      "name": "Lunch Break",
      "description": "30-minute lunch break",
      "created_at": "2024-01-05T12:00:00"
    }`

* * * * *

6\. Tasks
---------

### 6.1 Create Task

-   **Endpoint**: `POST /tasks`
-   **Description**: Submit a new task (User Story 1.2).
-   **Request Body**:

    json

    Copy code

    `{
      "submitter_id": 1,
      "pick_up_location": "Ward A",
      "drop_off_location": "Lab",
      "priority": "Urgent",
      "patient_item_details": "Blood samples",
      "additional_instructions": "Handle with care",
      "job_type_id": 1,  // e.g., "Equipment Delivery"
      "department_id": 2,
      "ward_id": 5
    }`

-   **Response** (success):

    json

    Copy code

    `{
      "task_id": 100,
      "submitter_id": 1,
      "priority": "Urgent",
      "status": "Pending",
      "created_at": "2024-01-10T09:00:00"
    }`

### 6.2 Get Task by ID

-   **Endpoint**: `GET /tasks/{task_id}`
-   **Description**: Retrieves detailed info about a single task.
-   **Response**:

    json

    Copy code

    `{
      "task_id": 100,
      "submitter_id": 1,
      "receiver_id": null,
      "pick_up_location": "Ward A",
      "drop_off_location": "Lab",
      "priority": "Urgent",
      "status": "Pending",
      "department_id": 2,
      "ward_id": 5,
      "created_at": "2024-01-10T09:00:00"
    }`

### 6.3 List Tasks (with Filtering)

-   **Endpoint**: `GET /tasks?status=Pending&priority=Urgent&department_id=2`
-   **Description**: Retrieves a filtered list of tasks based on query parameters (status, priority, etc.).
-   **Response**:

    json

    Copy code

    `[
      {
        "task_id": 100,
        "submitter_id": 1,
        "priority": "Urgent",
        "status": "Pending"
      }
    ]`

### 6.4 Update Task (Assign a Porter, Change Status)

-   **Endpoint**: `PUT /tasks/{task_id}`
-   **Description**: Updates task fields such as `receiver_id`, `status`, `priority`.
-   **Request Body**:

    json

    Copy code

    `{
      "receiver_id": 2,
      "status": "In Progress"
    }`

-   **Response** (success):

    json

    Copy code

    `{
      "message": "Task updated.",
      "task": {
        "task_id": 100,
        "receiver_id": 2,
        "status": "In Progress",
        "updated_at": "2024-01-10T09:30:00"
      }
    }`

### 6.5 Cancel Task

-   **Endpoint**: `POST /tasks/{task_id}/cancel`
-   **Description**: Cancels a task (User Story 1.3).
-   **Request Body** (optional reason):

    json

    Copy code

    `{
      "reason": "Task no longer needed."
    }`

-   **Response**:

    json

    Copy code

    `{
      "message": "Task canceled successfully.",
      "task_id": 100,
      "status": "Canceled"
    }`

* * * * *

7\. Task-Related Endpoints (Priority, Status, Attachments)
----------------------------------------------------------

### 7.1 Change Priority

-   **Endpoint**: `POST /tasks/{task_id}/priority`
-   **Description**: Logs a priority change (User Story 1.3).
-   **Request Body**:

    json

    Copy code

    `{
      "new_priority": "Emergency",
      "reason": "Patient condition deteriorated."
    }`

-   **Response**:

    json

    Copy code

    `{
      "message": "Priority updated.",
      "task_id": 100,
      "old_priority": "Urgent",
      "new_priority": "Emergency"
    }`

### 7.2 Post Status Update

-   **Endpoint**: `POST /tasks/{task_id}/status-updates`
-   **Description**: Creates a new status update record (e.g., "Waiting," "Completed").
-   **Request Body**:

    json

    Copy code

    `{
      "updated_by": 2,
      "status": "Completed",
      "comments": "Task finished successfully."
    }`

-   **Response**:

    json

    Copy code

    `{
      "status_update_id": 300,
      "task_id": 100,
      "updated_by": 2,
      "status": "Completed",
      "timestamp": "2024-01-10T10:00:00"
    }`

### 7.3 Upload Attachment

-   **Endpoint**: `POST /tasks/{task_id}/attachments`
-   **Description**: Upload a file associated with a task (e.g., an image).
-   **Request**: `multipart/form-data`
    -   **Fields**:
        -   `file`: The file to upload
        -   `uploaded_by`: The user ID
-   **Response**:

    json

    Copy code

    `{
      "attachment_id": 50,
      "task_id": 100,
      "file_path": "/uploads/task_100/img123.png",
      "uploaded_by": 2,
      "uploaded_at": "2024-01-10T10:05:00"
    }`

* * * * *

8\. Feedback, Messages, Notifications
-------------------------------------

### 8.1 Submit Feedback

-   **Endpoint**: `POST /tasks/{task_id}/feedback`
-   **Description**: Submits feedback (rating, comments) for a completed task (User Story 1.4).
-   **Request Body**:

    json

    Copy code

    `{
      "rating": 5,
      "comments": "Excellent service!",
      "submitted_by": 1
    }`

-   **Response**:

    json

    Copy code

    `{
      "feedback_id": 10,
      "task_id": 100,
      "rating": 5,
      "comments": "Excellent service!",
      "submitted_by": 1,
      "submitted_at": "2024-01-10T11:00:00"
    }`

### 8.2 Send Message

-   **Endpoint**: `POST /messages`
-   **Description**: Sends an in-app message from one user to another (User Story 2.3).
-   **Request Body**:

    json

    Copy code

    `{
      "task_id": 100,
      "sender_id": 2,
      "receiver_id": 1,
      "message": "I'm on my way!",
      "attachment_path": null
    }`

-   **Response**:

    json

    Copy code

    `{
      "message_id": 45,
      "task_id": 100,
      "sender_id": 2,
      "receiver_id": 1,
      "message": "I'm on my way!",
      "sent_at": "2024-01-10T09:45:00",
      "is_read": false
    }`

### 8.3 Get Notifications

-   **Endpoint**: `GET /notifications?user_id=1&is_read=false`
-   **Description**: Retrieves unread notifications for a given user (e.g., new tasks, messages).
-   **Response**:

    json

    Copy code

    `[
      {
        "notification_id": 10,
        "user_id": 1,
        "task_id": 100,
        "message": "Your task #100 has been assigned to Porter Jane.",
        "sent_at": "2024-01-10T09:35:00",
        "is_read": false
      }
    ]`

* * * * *

9\. Auditing & Reporting
------------------------

### 9.1 Get Audit Logs

-   **Endpoint**: `GET /audit-logs`
-   **Description**: Retrieves a list of all audit logs (with filters like `?user_id=2` or `?task_id=100`).
-   **Response**:

    json

    Copy code

    `[
      {
        "log_id": 1000,
        "action": "TASK_CREATE",
        "user_id": 1,
        "task_id": 100,
        "timestamp": "2024-01-10T09:00:00",
        "details": "Created new task",
        "old_values": null,
        "new_values": "{ \"task_id\": 100, \"status\": \"Pending\" }"
      }
    ]`

### 9.2 Generate Report

-   **Endpoint**: `POST /reports`
-   **Description**: Requests the generation of a report (e.g., CSV or PDF).
-   **Request Body**:

    json

    Copy code

    `{
      "generated_by": 1,
      "report_type": "DAILY_TASK_SUMMARY"
    }`

-   **Response**:

    json

    Copy code

    `{
      "report_id": 10,
      "generated_by": 1,
      "report_type": "DAILY_TASK_SUMMARY",
      "generated_at": "2024-01-10T23:59:00",
      "file_path": "/reports/daily_task_summary_2024-01-10.pdf"
    }`

* * * * *

10\. Staff Management (Availability, Shifts)
--------------------------------------------

### 10.1 Update Staff Availability

-   **Endpoint**: `POST /staff-availability`
-   **Description**: Set or update a porter's availability status (User Story 2.5).
-   **Request Body**:

    json

    Copy code

    `{
      "porter_id": 2,
      "status": "On Break",
      "break_requested": true,
      "break_type_id": 1 // e.g., "Lunch Break"
    }`

-   **Response**:

    json

    Copy code

    `{
      "availability_id": 50,
      "porter_id": 2,
      "status": "On Break",
      "break_requested": true,
      "approved": null,
      "updated_at": "2024-01-10T09:40:00"
    }`

### 10.2 Approve Break

-   **Endpoint**: `POST /staff-availability/{availability_id}/approve`
-   **Description**: Approves or rejects a break request (Operator role).
-   **Request Body**:

    json

    Copy code

    `{
      "approved": true
    }`

-   **Response**:

    json

    Copy code

    `{
      "availability_id": 50,
      "approved": true,
      "updated_at": "2024-01-10T09:45:00"
    }`

### 10.3 Create or End Shift

-   **Endpoint**: `POST /shifts`
-   **Description**: Starts or ends a shift for a user (User Story 3.4).
-   **Request Body** (start shift):

    json

    Copy code

    `{
      "user_id": 2,
      "shift_start": "2024-01-10T08:00:00"
    }`

-   **Request Body** (end shift):

    json

    Copy code

    `{
      "shift_id": 20,
      "shift_end": "2024-01-10T16:00:00"
    }`

-   **Response** (success):

    json

    Copy code

    `{
      "shift_id": 20,
      "user_id": 2,
      "shift_start": "2024-01-10T08:00:00",
      "shift_end": "2024-01-10T16:00:00"
    }`

* * * * *

11\. Public Links
-----------------

### 11.1 Create Public Link

-   **Endpoint**: `POST /public-links`
-   **Description**: Creates a public link for a station or form (User Story 1.1 - public access option).
-   **Request Body**:

    json

    Copy code

    `{
      "station_id": 1,
      "is_active": true
    }`

-   **Response**:

    json

    Copy code

    `{
      "link_id": 10,
      "link_url": "https://api.flow-taskmanager.com/v1/public/abc123",
      "station_id": 1,
      "is_active": true,
      "created_at": "2024-01-10T10:00:00"
    }`

### 11.2 Deactivate Public Link

-   **Endpoint**: `POST /public-links/{link_id}/deactivate`
-   **Description**: Turns off a public link.
-   **Response**:

    json

    Copy code

    `{
      "link_id": 10,
      "is_active": false
    }`

* * * * *

12\. Task Escalations
---------------------

### 12.1 Escalate Task

-   **Endpoint**: `POST /tasks/{task_id}/escalations`
-   **Description**: Escalates a task to higher-level attention (User Story 1.3 - upgrading severity or a separate path).
-   **Request Body**:

    json

    Copy code

    `{
      "escalated_by": 1,
      "reason": "Task not picked up within 30 minutes"
    }`

-   **Response**:

    json

    Copy code

    `{
      "escalation_id": 1,
      "task_id": 100,
      "escalated_by": 1,
      "reason": "Task not picked up within 30 minutes",
      "escalated_at": "2024-01-10T10:15:00"
    }`

* * * * *

13\. System Settings
--------------------

### 13.1 Get All Settings

-   **Endpoint**: `GET /system-settings`
-   **Description**: Retrieves all system-wide settings (User Story 3.3 - advanced admin).
-   **Response**:

    json

    Copy code

    `[
      {
        "setting_id": 1,
        "key": "DEFAULT_PRIORITY",
        "value": "Normal",
        "data_type": "string",
        "updated_at": "2024-01-10T07:00:00"
      },
      {
        "setting_id": 2,
        "key": "MAX_TASKS_PER_PORTER",
        "value": "5",
        "data_type": "int",
        "updated_at": "2024-01-10T07:10:00"
      }
    ]`

### 13.2 Update a Setting

-   **Endpoint**: `PUT /system-settings/{setting_id}`
-   **Description**: Updates the value of a system setting.
-   **Request Body**:

    json

    Copy code

    `{
      "value": "Emergency"
    }`

-   **Response**:

    json

    Copy code

    `{
      "setting_id": 1,
      "key": "DEFAULT_PRIORITY",
      "value": "Emergency",
      "data_type": "string",
      "updated_at": "2024-01-10T10:20:00"
    }`

* * * * *

14\. Incidents
--------------

### 14.1 Report Incident

-   **Endpoint**: `POST /tasks/{task_id}/incidents`
-   **Description**: Logs an incident related to a task (User Story 3.5 or Admin oversight).
-   **Request Body**:

    json

    Copy code

    `{
      "reported_by": 2,
      "description": "Equipment malfunction during transport",
      "severity": "High"
    }`

-   **Response**:

    json

    Copy code

    `{
      "incident_id": 10,
      "task_id": 100,
      "reported_by": 2,
      "description": "Equipment malfunction during transport",
      "severity": "High",
      "created_at": "2024-01-10T10:30:00"
    }`

* * * * *

15\. Vehicles
-------------

### 15.1 Create Vehicle

-   **Endpoint**: `POST /vehicles`
-   **Description**: Adds a new vehicle (e.g., cart, ambulance, etc.).
-   **Request Body**:

    json

    Copy code

    `{
      "registration_number": "ABC-123",
      "type": "Van",
      "status": "Available"
    }`

-   **Response**:

    json

    Copy code

    `{
      "vehicle_id": 5,
      "registration_number": "ABC-123",
      "type": "Van",
      "status": "Available",
      "created_at": "2024-01-10T11:00:00"
    }`

### 15.2 Assign Vehicle to User

-   **Endpoint**: `PUT /vehicles/{vehicle_id}`
-   **Description**: Updates the `assigned_to` field to link a Porter or staff user.
-   **Request Body**:

    json

    Copy code

    `{
      "assigned_to": 2,
      "status": "In Use"
    }`

-   **Response**:

    json

    Copy code

    `{
      "vehicle_id": 5,
      "assigned_to": 2,
      "status": "In Use",
      "updated_at": "2024-01-10T11:15:00"
    }`

* * * * *

16\. Versioning & Future Enhancements
-------------------------------------

-   **Version**: `v1`
-   **Planned Future Endpoints**:
    -   **Automatic Task Assignment**: `POST /tasks/auto-assign`
    -   **Advanced Reporting**: Enhanced filters and scheduling for reports.
    -   **Analytics Dashboard**: Real-time metrics on tasks and staff performance.

* * * * *

Summary
=======

The **Flow Task Management API** is designed to support the full lifecycle of tasks---submission, assignment, status updates, feedback, and auditing---across multiple user roles (Submitters, Porters, Operators, and Admins). It aligns with the **User Stories** you've defined:

-   **Submitters/Receivers**: Create and track tasks; provide feedback.
-   **Porterage Staff**: View assigned tasks, update statuses, request breaks.
-   **Operators**: Manage queues, staff availability, and escalations.
-   **Administrators**: Full auditing, reporting, system settings, user/role management.

Use this reference as a starting point; your actual implementation may include additional query parameters, pagination, rate-limiting, or custom error structures. For more details on models and relationships, refer to the **Flow Task Management Models** documentation and your database migration files.