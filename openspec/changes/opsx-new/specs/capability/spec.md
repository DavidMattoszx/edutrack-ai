# EduTrack AI System Specification

## Purpose
Define the full EduTrack AI system requirements for authentication, subject management, academic task tracking, and Streamlit dashboard reporting. The specification ensures secure user ownership, overdue logic, task prioritization, and an actionable user interface.

## ADDED Requirements

### Requirement: Secure JWT authentication and user session management
The system SHALL support signup, login, JWT session persistence, and token expiration for authenticated users.
#### Scenario: User signs up and logs in
- **WHEN** a new user signs up with valid credentials
- **THEN** the system creates a user account and issues a JWT token

#### Scenario: User session expires
- **WHEN** a user’s JWT token expires
- **THEN** the system denies access and requires re-authentication

### Requirement: User profile edit and password reset
The system SHALL allow authenticated users to update their name and email and reset their password securely.
#### Scenario: Authenticated user updates profile
- **WHEN** a logged-in user updates their name or email
- **THEN** the system saves the changes only for that user

#### Scenario: User resets password
- **WHEN** a user requests a password reset
- **THEN** the system validates the request and allows secure password change

### Requirement: Subjects CRUD scoped to authenticated user
The system SHALL provide create, read, update, and delete operations for subjects linked to the authenticated user.
#### Scenario: User manages their subjects
- **WHEN** a user performs subject CRUD actions
- **THEN** only subjects with `user_id == $auth.id` are accessed or modified

### Requirement: Prevent duplicate subjects per user
The system SHALL prevent creating duplicate subjects with the same name for the same authenticated user.
#### Scenario: Duplicate subject validation
- **WHEN** a user attempts to create a subject with a name they already use
- **THEN** the system rejects the request with a validation error

### Requirement: Hybrid subject search with overdue filters
The system SHALL support searching subjects by partial name and filtering by overdue task status.
#### Scenario: Search for subjects by name or overdue tasks
- **WHEN** a user searches by subject name or selects overdue filter
- **THEN** the system returns secure results scoped to that user

### Requirement: Academic task CRUD with subject and user associations
The system SHALL allow task creation, update, deletion, and retrieval tied to a subject and authenticated user.
#### Scenario: User creates a task for a subject
- **WHEN** a user creates a task under a subject
- **THEN** the task is stored with the correct `subject_id` and `user_id`

### Requirement: Task status filtering and overdue detection
The system SHALL support task filters for Pendente, Em andamento, Concluída, and detect overdue tasks when `due_date < now`.
#### Scenario: View overdue and pending tasks
- **WHEN** a user views tasks by status
- **THEN** overdue tasks are flagged and separate from completed tasks

### Requirement: Task priority and archive discipline support
The system SHALL include task priority levels (Baixa, Média, Alta) and allow archiving completed disciplines.
#### Scenario: Set task priority and archive a discipline
- **WHEN** a user assigns task priority and archives a completed subject
- **THEN** the task priority is stored and the subject is marked as archived

### Requirement: Streamlit dashboard and reporting UI
The system SHALL provide a dashboard that shows active subjects, pending/overdue tasks, upcoming deadlines, progress metrics, and CSV report export.
#### Scenario: User views dashboard after login
- **WHEN** a user logs in successfully
- **THEN** the dashboard displays summary stats, upcoming tasks, and progress indicators

#### Scenario: User exports task report
- **WHEN** a user requests CSV export from reports
- **THEN** the system returns a CSV file with the selected task history data
