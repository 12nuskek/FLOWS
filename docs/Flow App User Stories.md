
# User Stories for Flow Task Management App

## 1. Submitters/Receivers

### 1.1 User Authentication & Access

- **User Story**  
  *As a Submitter/Receiver, I want to log into the Flow application (or access it publicly, depending on settings), so that I can securely submit and review tasks.*
  
- **Details & Acceptance Criteria**  
  - **Username & Password Access**  
    - Must prompt for username and password for protected stations.  
    - Successful login grants access to submission functionalities.  
    - Unsuccessful login attempts prompt an error message and log the attempt.  
  - **Public Access (if configured)**  
    - Certain stations can be publicly accessible without credentials (based on operator settings).  
    - Public pages are uniquely identifiable via a public link (URL).  
    - No login is required for public stations, but submission logs are still tracked.  

---

### 1.2 Task Submission

- **User Story**  
  *As a Submitter (e.g., Nurse/Doctor/Admin Staff), I want to submit a task, so that Porterage Staff can attend to my request.*

- **Details & Acceptance Criteria**  
  - **Task Request Form**  
    - Must include fields such as:  
      - Pick-up location  
      - Drop-off location  
      - Priority (e.g., normal, urgent, emergency)  
      - Patient or item details (optional if relevant)  
      - Additional instructions/comments  
    - Mandatory fields must be clearly indicated.  
  - **Confirmation of Submission**  
    - Once submitted, I should see a confirmation screen indicating the job number or reference ID.  
    - Confirmation is also sent via email or in-app notification (if configured).  
  - **Queue Placement**  
    - The submitted task should automatically enter the Operators’ job queue.  
    - I should be able to see a “pending” status until a Porterage Staff member is assigned.  

---

### 1.3 Viewing and Managing Submitted Tasks

- **User Story**  
  *As a Submitter/Receiver, I want to view and track previously submitted tasks, so that I can see the status and history of my requests.*

- **Details & Acceptance Criteria**  
  - **Historical Job List**  
    - Displays a list of all submitted tasks for the station or user.  
    - Includes current status (e.g., new, in-progress, completed, canceled).  
  - **Upgrade Severity**  
    - Must be able to upgrade a job’s severity (e.g., from normal to urgent) if needed.  
    - The system should notify the Porterage Staff and Operators of the change in priority.  
  - **Cancel a Job**  
    - Option to cancel a job if it is no longer required.  
    - A confirmation prompt appears before final cancellation.  
    - Cancellation reason can be captured (optional).  

---

### 1.4 Job Review & Feedback

- **User Story**  
  *As a Submitter/Receiver, I want to leave feedback on a completed job, so that I can review the quality of the service.*

- **Details & Acceptance Criteria**  
  - **Quality Review**  
    - Submitter can rate the job (e.g., 1–5 stars or rating scale).  
    - Optional text feedback for improvements.  
  - **Data Logging**  
    - Ratings and comments are stored for reporting and quality assurance.  
  - **Historical Records**  
    - Once a job is completed, the feedback remains visible in job history.  

---

## 2. Porterage Staff (Users)

### 2.1 Receive Jobs via Mobile

- **User Story**  
  *As a Porterage Staff member, I want to see new tasks on my mobile device, so that I can respond to them efficiently.*

- **Details & Acceptance Criteria**  
  - **Push Notifications**  
    - Mobile app notifies the user of newly assigned or available tasks.  
    - Must show relevant job details (location, priority, etc.).  
  - **Job Acceptance**  
    - Option to accept or decline a job based on availability.  
    - Declined jobs return to the Operator’s queue.  

---

### 2.2 Job Status Updates

- **User Story**  
  *As a Porterage Staff member, I want to update the status of a job (e.g., in-progress, completed), so that the system accurately reflects my workflow.*

- **Details & Acceptance Criteria**  
  - **Update Mechanism**  
    - Buttons or dropdowns to change job status: “In Progress,” “Waiting,” “Completed,” etc.  
    - Real-time updates that notify Operators and, optionally, the Submitter.  
  - **Timestamp and Audit Trail**  
    - Each status change is timestamped for future auditing.  

---

### 2.3 Communication with Operators and Submitters

- **User Story**  
  *As a Porterage Staff member, I want to message the Operator (or Submitter) within the app, so that I can clarify task details.*

- **Details & Acceptance Criteria**  
  - **In-App Messaging**  
    - Chat window or messaging function that allows one-to-one or group communication (e.g., operator, submitter, porter).  
    - Must include attachments (pictures, documents) if needed.  
  - **Notifications**  
    - When a new message arrives, a push notification should appear.  
  - **Thread Storage**  
    - All messages are stored in the job record for historical reference.  

---

### 2.4 Job History

- **User Story**  
  *As a Porterage Staff member, I want to view my job history, so that I can track completed tasks and refer to them if needed.*

- **Details & Acceptance Criteria**  
  - **Historical Log**  
    - Displays job ID, request time, completion time, and comments/feedback.  
  - **Search & Filter**  
    - Ability to search past tasks by location, date, or other attributes.  
  - **Performance Metrics**  
    - Optional: Display personal performance statistics (e.g., average completion time).  

---

### 2.5 Break Requests

- **User Story**  
  *As a Porterage Staff member, I want to request a break, so that I can have Operator-approved downtime.*

- **Details & Acceptance Criteria**  
  - **Break Request Submission**  
    - Button or form to request break with reason or type of break (e.g., lunch, short rest).  
  - **Approval Workflow**  
    - Operators must see a pending approval request.  
    - Approved or rejected requests are communicated back to the Staff member.  
  - **Availability Indicator**  
    - If on break, the Staff member should not receive new job assignments until back on duty.  

---

## 3. Operators

### 3.1 Viewing and Managing Incoming Tasks

- **User Story**  
  *As an Operator, I want to see all submitted tasks in a queue, so that I can efficiently delegate them to Porterage Staff.*

- **Details & Acceptance Criteria**  
  - **Task Queue**  
    - Displays new, in-progress, and unassigned tasks in chronological order.  
    - Filters for priority or location (e.g., urgent tasks at the top).  
  - **Mark as Read/Unread**  
    - Operator can mark tasks as “read” to indicate it’s being handled.  
  - **Bulk Actions**  
    - Option to select multiple tasks and assign or mark them quickly.  

---

### 3.2 Delegating Jobs to Porterage Staff

- **User Story**  
  *As an Operator, I want to assign tasks to specific Porterage Staff members, so that I can ensure tasks are handled by the appropriate personnel.*

- **Details & Acceptance Criteria**  
  - **Staff Availability**  
    - System displays which staff members are currently on shift and not on break.  
  - **Manual Assignment**  
    - Operator chooses a staff member from a dropdown or list.  
    - Optionally, staff members can accept/decline the assignment.  
  - **Automatic Assignment (Optional Future Feature)**  
    - Could have an algorithm to auto-assign based on location/availability. (Placeholder for future enhancement.)  

---

### 3.3 User and Role Management (CRUD)

- **User Story**  
  *As an Operator, I want the ability to create, read, update, and delete user accounts, so that I can manage who has access to the Flow system.*

- **Details & Acceptance Criteria**  
  - **CRUD for Users**  
    - Create new Porterage Staff user accounts with roles and permissions.  
    - Update user details, reset passwords, and deactivate accounts as needed.  
    - Delete accounts that are no longer required.  
  - **CRUD for Operators**  
    - The ability to create or promote certain users to Operator roles.  
    - Control over operator-level permissions.  
  - **CRUD for Submitters**  
    - Manage Submitter accounts or station profiles.  
    - Enable/disable public links.  
  - **Job Types**  
    - Add/edit/delete job types (e.g., “Patient Transfer,” “Equipment Delivery”).  
  - **Placeholder Features**  
    - Sections or placeholders for future expansions (e.g., advanced scheduling algorithms).  

---

### 3.4 Operator Shifts & Break Approvals

- **User Story**  
  *As an Operator, I want to sign Porterage Staff on and off shift, and approve break requests, so that I can track staffing levels.*

- **Details & Acceptance Criteria**  
  - **Sign On/Sign Off**  
    - Operator can mark a staff member as “on duty” or “off duty.”  
    - Staff member cannot receive jobs if off duty.  
  - **Break Approval**  
    - Operator sees pending break requests in a dashboard.  
    - Approve or reject with an optional message.  

---

### 3.5 Super User Access over Tasks

- **User Story**  
  *As an Operator with super user privileges, I want to view and modify any task, so that I can handle special situations or correct mistakes.*

- **Details & Acceptance Criteria**  
  - **Task Editing**  
    - Update job details (location, priority, assigned staff) as needed.  
  - **Audit Trail**  
    - Any changes made by the super user are timestamped and logged for record-keeping.  
  - **Emergency Override**  
    - For critical changes (e.g., reassign urgent tasks), the system should highlight these updates to staff.  

---

## 4. Auditing & Reporting (Cross-Role)

### User Story

*As an Administrator or compliance officer, I want to view a detailed history of all tasks and user actions, so that I can ensure accountability and transparency.*

- **Details & Acceptance Criteria**  
  - **Audit Trails**  
    - Log of who created, assigned, updated, or canceled tasks.  
    - Includes timestamps, user IDs, and reason codes (if any).  
  - **Historical Reporting**  
    - Generate reports on tasks by date, priority, completion time, etc.  
    - Export to CSV/PDF for external analysis.  
  - **Access Control**  
    - Only authorized roles (Operators or Admin-level roles) can view the full audit logs.  
