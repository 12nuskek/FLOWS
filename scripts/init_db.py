import sqlite3
import os
from pathlib import Path

def init_db():
    # Create the instance directory if it doesn't exist
    instance_path = Path('instance')
    instance_path.mkdir(exist_ok=True)
    
    # Database file path
    db_path = instance_path / 'flow.db'
    
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute('PRAGMA foreign_keys = ON;')
    
    # Create Roles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Roles (
        role_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        name      TEXT UNIQUE NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create Permissions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Permissions (
        permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT UNIQUE NOT NULL,
        description   TEXT,
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create RolePermissions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RolePermissions (
        role_permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_id            INTEGER NOT NULL,
        permission_id      INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES Roles(role_id),
        FOREIGN KEY (permission_id) REFERENCES Permissions(permission_id)
    )
    ''')

    # Create Departments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT NOT NULL,
        location      TEXT,
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Wards table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Wards (
        ward_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        department_id INTEGER NOT NULL,
        name          TEXT NOT NULL,
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (department_id) REFERENCES Departments(department_id)
    )
    ''')

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        username       TEXT UNIQUE NOT NULL,
        password_hash  TEXT NOT NULL,
        role_id        INTEGER REFERENCES Roles(role_id),
        department_id  INTEGER REFERENCES Departments(department_id),
        is_active      BOOLEAN DEFAULT 1,
        email          TEXT UNIQUE,
        phone          TEXT,
        created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create UserProfiles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserProfiles (
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
    )
    ''')

    # Create JobTypes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS JobTypes (
        job_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        description TEXT,
        is_active   BOOLEAN DEFAULT 1,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create BreakTypes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BreakTypes (
        break_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT NOT NULL,
        description   TEXT,
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tasks (
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
        
        job_type_id           INTEGER REFERENCES JobTypes(job_type_id),
        estimated_duration    INTEGER,
        actual_duration       INTEGER,
        start_time            TIMESTAMP,
        end_time             TIMESTAMP,

        department_id         INTEGER REFERENCES Departments(department_id),
        ward_id              INTEGER REFERENCES Wards(ward_id),

        created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (submitter_id) REFERENCES Users(user_id),
        FOREIGN KEY (receiver_id)  REFERENCES Users(user_id)
    )
    ''')

    # Create PriorityChanges table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PriorityChanges (
        change_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id      INTEGER NOT NULL,
        changed_by   INTEGER NOT NULL,
        old_priority TEXT NOT NULL,
        new_priority TEXT NOT NULL,
        reason       TEXT,
        changed_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id)    REFERENCES Tasks(task_id),
        FOREIGN KEY (changed_by) REFERENCES Users(user_id)
    )
    ''')

    # Create TaskStatusUpdates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TaskStatusUpdates (
        status_update_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id          INTEGER NOT NULL,
        updated_by       INTEGER NOT NULL,
        status           TEXT NOT NULL,
        timestamp        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        comments         TEXT,
        FOREIGN KEY (task_id)    REFERENCES Tasks(task_id),
        FOREIGN KEY (updated_by) REFERENCES Users(user_id)
    )
    ''')

    # Create TaskAttachments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TaskAttachments (
        attachment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id       INTEGER NOT NULL,
        file_path     TEXT NOT NULL,
        uploaded_by   INTEGER NOT NULL,
        uploaded_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        file_size     INTEGER,
        file_type     TEXT,
        FOREIGN KEY (task_id)    REFERENCES Tasks(task_id),
        FOREIGN KEY (uploaded_by) REFERENCES Users(user_id)
    )
    ''')

    # Create Feedback table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Feedback (
        feedback_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id      INTEGER NOT NULL,
        rating       INTEGER CHECK(rating BETWEEN 1 AND 5),
        comments     TEXT,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        submitted_by INTEGER REFERENCES Users(user_id),
        FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
    )
    ''')

    # Create Messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Messages (
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
    )
    ''')

    # Create Notifications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Notifications (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id         INTEGER NOT NULL,
        task_id         INTEGER,
        message         TEXT NOT NULL,
        sent_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_read         BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
    )
    ''')

    # Create AuditLogs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AuditLogs (
        log_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        action     TEXT NOT NULL,
        user_id    INTEGER NOT NULL,
        task_id    INTEGER,
        timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        details    TEXT,
        old_values TEXT,
        new_values TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
    )
    ''')

    # Create Reports table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reports (
        report_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        generated_by INTEGER NOT NULL,
        report_type  TEXT NOT NULL,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        file_path    TEXT NOT NULL,
        FOREIGN KEY (generated_by) REFERENCES Users(user_id)
    )
    ''')

    # Create StaffAvailability table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS StaffAvailability (
        availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
        porter_id       INTEGER NOT NULL,
        status          TEXT CHECK(status IN ('On Duty','Off Duty','On Break')) NOT NULL,
        break_requested BOOLEAN DEFAULT 0,
        approved        BOOLEAN DEFAULT NULL,
        updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        break_type_id   INTEGER REFERENCES BreakTypes(break_type_id),
        FOREIGN KEY (porter_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Shifts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shifts (
        shift_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        shift_start TIMESTAMP NOT NULL,
        shift_end   TIMESTAMP,
        is_active  BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Create PublicLinks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PublicLinks (
        link_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        link_url   TEXT UNIQUE NOT NULL,
        station_id INTEGER NOT NULL,
        is_active  BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (station_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Escalations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Escalations (
        escalation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id       INTEGER NOT NULL,
        escalated_by  INTEGER NOT NULL,
        reason        TEXT NOT NULL,
        escalated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id)      REFERENCES Tasks(task_id),
        FOREIGN KEY (escalated_by) REFERENCES Users(user_id)
    )
    ''')

    # Create SystemSettings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SystemSettings (
        setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
        key        TEXT UNIQUE NOT NULL,
        value      TEXT NOT NULL,
        data_type  TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Incidents table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Incidents (
        incident_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id      INTEGER NOT NULL,
        reported_by  INTEGER NOT NULL,
        description  TEXT NOT NULL,
        severity     TEXT CHECK(severity IN ('Low','Medium','High','Critical')) DEFAULT 'Low',
        created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id)     REFERENCES Tasks(task_id),
        FOREIGN KEY (reported_by) REFERENCES Users(user_id)
    )
    ''')

    # Create Vehicles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vehicles (
        vehicle_id          INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_number TEXT NOT NULL,
        type               TEXT NOT NULL,
        status             TEXT CHECK(status IN ('Available','In Use','Under Maintenance','Retired'))
                          DEFAULT 'Available',
        assigned_to        INTEGER,
        created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (assigned_to) REFERENCES Users(user_id)
    )
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 