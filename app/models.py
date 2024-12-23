# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'Roles'

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to RolePermissions
    role_permissions = db.relationship('RolePermission', backref='role', lazy=True)


class Permission(db.Model):
    __tablename__ = 'Permissions'

    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to RolePermissions
    role_permissions = db.relationship('RolePermission', backref='permission', lazy=True)


class RolePermission(db.Model):
    __tablename__ = 'RolePermissions'

    role_permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.role_id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('Permissions.permission_id'), nullable=False)


class Department(db.Model):
    __tablename__ = 'Departments'

    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Wards
    wards = db.relationship('Ward', backref='department', lazy=True)

    # Relationship to Users
    users = db.relationship('User', backref='department', lazy=True)

    # Relationship to Tasks (if tasks are associated directly to a department)
    tasks = db.relationship('Task', backref='department', lazy=True)


class Ward(db.Model):
    __tablename__ = 'Wards'

    ward_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.department_id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Tasks (if tasks are associated to wards)
    tasks = db.relationship('Task', backref='ward', lazy=True)


class JobType(db.Model):
    __tablename__ = 'JobTypes'

    job_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Tasks
    tasks = db.relationship('Task', backref='job_type', lazy=True)


class BreakType(db.Model):
    __tablename__ = 'BreakTypes'

    break_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to StaffAvailability
    staff_availabilities = db.relationship('StaffAvailability', backref='break_type', lazy=True)


class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('Roles.role_id'), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.department_id'), nullable=True)

    is_active = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    phone = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to UserProfile
    profile = db.relationship('UserProfile', backref='user', uselist=False)

    # Relationship to Tasks as a submitter
    submitted_tasks = db.relationship(
        'Task',
        foreign_keys='Task.submitter_id',
        backref='submitter',
        lazy=True
    )
    # Relationship to Tasks as a receiver
    received_tasks = db.relationship(
        'Task',
        foreign_keys='Task.receiver_id',
        backref='receiver',
        lazy=True
    )

    # Relationship to PriorityChanges
    priority_changes = db.relationship('PriorityChange', backref='changed_by_user', lazy=True)

    # Relationship to TaskStatusUpdates
    status_updates = db.relationship('TaskStatusUpdate', backref='updated_by_user', lazy=True)

    # Relationship to TaskAttachments
    task_attachments = db.relationship('TaskAttachment', backref='uploaded_by_user', lazy=True)

    # Relationship to Feedback
    feedback_submitted = db.relationship('Feedback', backref='submitted_by_user', lazy=True)

    # Relationship to Messages as a sender
    messages_sent = db.relationship(
        'Message',
        foreign_keys='Message.sender_id',
        backref='sender',
        lazy=True
    )
    # Relationship to Messages as a receiver
    messages_received = db.relationship(
        'Message',
        foreign_keys='Message.receiver_id',
        backref='receiver',
        lazy=True
    )

    # Relationship to Notifications
    notifications = db.relationship('Notification', backref='user', lazy=True)

    # Relationship to AuditLogs
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)

    # Relationship to Reports
    reports = db.relationship('Report', backref='generated_by_user', lazy=True)

    # Relationship to StaffAvailability
    staff_availabilities = db.relationship('StaffAvailability', backref='porter', lazy=True)

    # Relationship to Shifts
    shifts = db.relationship('Shift', backref='staff_member', lazy=True)

    # Relationship to PublicLinks if the user is acting as a station
    public_links = db.relationship('PublicLink', backref='station', lazy=True)

    # Relationship to Escalations
    escalations = db.relationship('Escalation', backref='escalated_by_user', lazy=True)

    # Relationship to Incidents
    incidents_reported = db.relationship('Incident', backref='reported_by_user', lazy=True)

    # Relationship to Vehicles (for assigned_to)
    vehicles_assigned = db.relationship('Vehicle', backref='assigned_user', lazy=True)


class UserProfile(db.Model):
    __tablename__ = 'UserProfiles'

    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class Task(db.Model):
    __tablename__ = 'Tasks'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    submitter_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=True)

    pick_up_location = db.Column(db.String(255), nullable=False)
    drop_off_location = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.String(50), nullable=False, default='Normal')  # Normal, Urgent, Emergency
    patient_item_details = db.Column(db.Text, nullable=True)
    additional_instructions = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')  # Pending, In Progress, ...

    job_type_id = db.Column(db.Integer, db.ForeignKey('JobTypes.job_type_id'), nullable=True)
    estimated_duration = db.Column(db.Integer, nullable=True)
    actual_duration = db.Column(db.Integer, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)

    department_id = db.Column(db.Integer, db.ForeignKey('Departments.department_id'), nullable=True)
    ward_id = db.Column(db.Integer, db.ForeignKey('Wards.ward_id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to PriorityChanges
    priority_changes = db.relationship('PriorityChange', backref='task', lazy=True)

    # Relationship to TaskStatusUpdates
    status_updates = db.relationship('TaskStatusUpdate', backref='task', lazy=True)

    # Relationship to TaskAttachments
    attachments = db.relationship('TaskAttachment', backref='task', lazy=True)

    # Relationship to Feedback
    feedback = db.relationship('Feedback', backref='task', lazy=True)

    # Relationship to Messages
    messages = db.relationship('Message', backref='task', lazy=True)

    # Relationship to Notifications
    notifications = db.relationship('Notification', backref='task', lazy=True)

    # Relationship to AuditLogs
    audit_logs = db.relationship('AuditLog', backref='task', lazy=True)

    # Relationship to Escalations
    escalations = db.relationship('Escalation', backref='task', lazy=True)

    # Relationship to Incidents
    incidents = db.relationship('Incident', backref='task', lazy=True)


class PriorityChange(db.Model):
    __tablename__ = 'PriorityChanges'

    change_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.task_id'), nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    old_priority = db.Column(db.String(50), nullable=False)
    new_priority = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)


class TaskStatusUpdate(db.Model):
    __tablename__ = 'TaskStatusUpdates'

    status_update_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.task_id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(db.Text, nullable=True)


class TaskAttachment(db.Model):
    __tablename__ = 'TaskAttachments'

    attachment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.task_id'), nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    file_size = db.Column(db.Integer, nullable=True)
    file_type = db.Column(db.String(100), nullable=True)


class Feedback(db.Model):
    __tablename__ = 'Feedback'

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.task_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # 1 to 5
    comments = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_by = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=True)


class Message(db.Model):
    __tablename__ = 'Messages'

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.task_id'), nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)

    message = db.Column(db.Text, nullable=False)
    attachment_path = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


class Notification(db.Model):
    __tablename__ = 'Notifications'

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.task_id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


class AuditLog(db.Model):
    __tablename__ = 'AuditLogs'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.task_id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)
    old_values = db.Column(db.Text, nullable=True)
    new_values = db.Column(db.Text, nullable=True)


class Report(db.Model):
    __tablename__ = 'Reports'

    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    generated_by = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    report_type = db.Column(db.String(100), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.Text, nullable=False)


class StaffAvailability(db.Model):
    __tablename__ = 'StaffAvailability'

    availability_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    porter_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='On Duty')  # On Duty, Off Duty, On Break
    break_requested = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=None)  # can be True/False/None
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    break_type_id = db.Column(db.Integer, db.ForeignKey('BreakTypes.break_type_id'), nullable=True)


class Shift(db.Model):
    __tablename__ = 'Shifts'

    shift_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    shift_start = db.Column(db.DateTime, nullable=False)
    shift_end = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PublicLink(db.Model):
    __tablename__ = 'PublicLinks'

    link_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link_url = db.Column(db.String(255), unique=True, nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Escalation(db.Model):
    __tablename__ = 'Escalations'

    escalation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.task_id'), nullable=False)
    escalated_by = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    escalated_at = db.Column(db.DateTime, default=datetime.utcnow)


class SystemSetting(db.Model):
    __tablename__ = 'SystemSettings'

    setting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    data_type = db.Column(db.String(50), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class Incident(db.Model):
    __tablename__ = 'Incidents'

    incident_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.task_id'), nullable=False)
    reported_by = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50), nullable=False, default='Low')  # Low, Medium, High, Critical
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class Vehicle(db.Model):
    __tablename__ = 'Vehicles'

    vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registration_number = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)  # e.g., 'Van','Cart','Ambulance'
    status = db.Column(db.String(100), nullable=False, default='Available')  # 'Available','In Use','Under Maintenance','Retired'

    assigned_to = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
