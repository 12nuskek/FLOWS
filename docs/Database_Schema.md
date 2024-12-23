-- Enable foreign keys (for SQLite; in other DBs, foreign keys are on by default)
PRAGMA foreign_keys = ON;

------------------------------------------------------------------------------
-- 1. Roles, Permissions, and RolePermissions
------------------------------------------------------------------------------

CREATE TABLE Roles (
    role_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Permissions (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT UNIQUE NOT NULL,
    description   TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE RolePermissions (
    role_permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id            INTEGER NOT NULL,
    permission_id      INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id),
    FOREIGN KEY (permission_id) REFERENCES Permissions(permission_id)
);

------------------------------------------------------------------------------
-- 2. Organizational Structure: Departments, Wards
------------------------------------------------------------------------------

CREATE TABLE Departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    location      TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Wards (
    ward_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    name          TEXT NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

------------------------------------------------------------------------------
-- 3. JobTypes and BreakTypes
------------------------------------------------------------------------------

CREATE TABLE JobTypes (
    job_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT,
    is_active   BOOLEAN DEFAULT 1,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE BreakTypes (
    break_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    description   TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

------------------------------------------------------------------------------
-- 4. Users and UserProfiles
------------------------------------------------------------------------------

CREATE TABLE Users (
    user_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username       TEXT UNIQUE NOT NULL,
    password_hash  TEXT NOT NULL,
    -- Reference to Roles table rather than storing text-based role
    role_id        INTEGER REFERENCES Roles(role_id),
    
    department_id  INTEGER REFERENCES Departments(department_id),
    is_active      BOOLEAN DEFAULT 1,
    email          TEXT UNIQUE,
    phone          TEXT,

    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE UserProfiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    first_name TEXT,
    last_name  TEXT,
    address    TEXT,
    phone      TEXT,
    email      TEXT UNIQUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

------------------------------------------------------------------------------
-- 5. Tasks and Related Tables (Status Updates, Attachments, etc.)
------------------------------------------------------------------------------

CREATE TABLE Tasks (
    task_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    submitter_id          INTEGER NOT NULL,
    receiver_id           INTEGER,
    pick_up_location      TEXT NOT NULL,
    drop_off_location     TEXT NOT NULL,
    priority              TEXT CHECK (priority IN ('Normal','Urgent','Emergency')) NOT NULL,
    patient_item_details  TEXT,
    additional_instructions TEXT,
    status                TEXT CHECK(status IN ('Pending','In Progress','Waiting','Completed','Canceled'))
                          DEFAULT 'Pending',
    
    -- New columns for scheduling and job type
    job_type_id           INTEGER REFERENCES JobTypes(job_type_id),
    estimated_duration    INTEGER,
    actual_duration       INTEGER,
    start_time            TIMESTAMP,
    end_time              TIMESTAMP,

    -- Optionally link tasks to a department or ward
    department_id         INTEGER REFERENCES Departments(department_id),
    ward_id               INTEGER REFERENCES Wards(ward_id),

    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (submitter_id) REFERENCES Users(user_id),
    FOREIGN KEY (receiver_id)  REFERENCES Users(user_id)
);

-- Table to track changes to priority
CREATE TABLE PriorityChanges (
    change_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id      INTEGER NOT NULL,
    changed_by   INTEGER NOT NULL,
    old_priority TEXT NOT NULL,
    new_priority TEXT NOT NULL,
    reason       TEXT,
    changed_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id)    REFERENCES Tasks(task_id),
    FOREIGN KEY (changed_by) REFERENCES Users(user_id)
);

CREATE TABLE TaskStatusUpdates (
    status_update_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id          INTEGER NOT NULL,
    updated_by       INTEGER NOT NULL,
    status           TEXT NOT NULL,
    timestamp        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comments         TEXT,
    FOREIGN KEY (task_id)    REFERENCES Tasks(task_id),
    FOREIGN KEY (updated_by) REFERENCES Users(user_id)
);

CREATE TABLE TaskAttachments (
    attachment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL,
    file_path     TEXT NOT NULL,
    uploaded_by   INTEGER NOT NULL,
    uploaded_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Extended file metadata
    file_size     INTEGER,
    file_type     TEXT,

    FOREIGN KEY (task_id)    REFERENCES Tasks(task_id),
    FOREIGN KEY (uploaded_by) REFERENCES Users(user_id)
);

------------------------------------------------------------------------------
-- 6. Feedback, Messages, Notifications
------------------------------------------------------------------------------

CREATE TABLE Feedback (
    feedback_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id      INTEGER NOT NULL,
    rating       INTEGER CHECK(rating BETWEEN 1 AND 5),
    comments     TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_by INTEGER REFERENCES Users(user_id),
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
);

CREATE TABLE Messages (
    message_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER,
    sender_id     INTEGER NOT NULL,
    receiver_id   INTEGER NOT NULL,
    message       TEXT NOT NULL,
    attachment_path TEXT,
    sent_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read       BOOLEAN DEFAULT 0,
    FOREIGN KEY (task_id)    REFERENCES Tasks(task_id),
    FOREIGN KEY (sender_id)  REFERENCES Users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
);

CREATE TABLE Notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    task_id         INTEGER,
    message         TEXT NOT NULL,
    sent_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read         BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
);

------------------------------------------------------------------------------
-- 7. Auditing and Reporting
------------------------------------------------------------------------------

CREATE TABLE AuditLogs (
    log_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    action     TEXT NOT NULL,
    user_id    INTEGER NOT NULL,
    task_id    INTEGER,
    timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details    TEXT,
    -- Store old & new values for more detailed auditing
    old_values TEXT,
    new_values TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
);

CREATE TABLE Reports (
    report_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    generated_by INTEGER NOT NULL,
    report_type  TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path    TEXT NOT NULL,
    FOREIGN KEY (generated_by) REFERENCES Users(user_id)
);

------------------------------------------------------------------------------
-- 8. Porter / Staff Management: Availability, Shifts, etc.
------------------------------------------------------------------------------

CREATE TABLE StaffAvailability (
    availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
    porter_id       INTEGER NOT NULL,
    status          TEXT CHECK(status IN ('On Duty','Off Duty','On Break')) NOT NULL,
    break_requested BOOLEAN DEFAULT 0,
    approved        BOOLEAN DEFAULT NULL,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    break_type_id   INTEGER REFERENCES BreakTypes(break_type_id),
    FOREIGN KEY (porter_id) REFERENCES Users(user_id)
);

CREATE TABLE Shifts (
    shift_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    shift_start TIMESTAMP NOT NULL,
    shift_end   TIMESTAMP,
    is_active  BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

------------------------------------------------------------------------------
-- 9. Public Links
------------------------------------------------------------------------------

CREATE TABLE PublicLinks (
    link_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    link_url   TEXT UNIQUE NOT NULL,
    station_id INTEGER NOT NULL,
    is_active  BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES Users(user_id)
);

------------------------------------------------------------------------------
-- 10. Task Escalations
------------------------------------------------------------------------------

CREATE TABLE Escalations (
    escalation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL,
    escalated_by  INTEGER NOT NULL,
    reason        TEXT NOT NULL,
    escalated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id)      REFERENCES Tasks(task_id),
    FOREIGN KEY (escalated_by) REFERENCES Users(user_id)
);

------------------------------------------------------------------------------
-- 11. System Settings
------------------------------------------------------------------------------

CREATE TABLE SystemSettings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    key        TEXT UNIQUE NOT NULL,
    value      TEXT NOT NULL,
    data_type  TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

------------------------------------------------------------------------------
-- 12. Incidents
------------------------------------------------------------------------------

CREATE TABLE Incidents (
    incident_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id      INTEGER NOT NULL,
    reported_by  INTEGER NOT NULL,
    description  TEXT NOT NULL,
    severity     TEXT CHECK(severity IN ('Low','Medium','High','Critical')) DEFAULT 'Low',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id)     REFERENCES Tasks(task_id),
    FOREIGN KEY (reported_by) REFERENCES Users(user_id)
);

------------------------------------------------------------------------------
-- 13. Vehicles
------------------------------------------------------------------------------

CREATE TABLE Vehicles (
    vehicle_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT NOT NULL,
    type                TEXT NOT NULL,  -- e.g., 'Van','Cart','Ambulance', etc.
    status              TEXT CHECK(status IN ('Available','In Use','Under Maintenance','Retired'))
                        DEFAULT 'Available',
    assigned_to         INTEGER,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_to) REFERENCES Users(user_id)
);
