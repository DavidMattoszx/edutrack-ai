# activity-grades Specification

## Purpose
Define the database structure and API for managing activity grades in EduTrack AI, allowing teachers to assign grades to students for specific activities.

## ADDED Requirements

### Requirement: Create activity_grades table
The system SHALL store activity grade information including activity, student, grade value, and teacher who assigned it.

#### Scenario: Teacher assigns grade to student activity
- **WHEN** teacher assigns a grade to a student's activity submission
- **THEN** system stores the grade with activity_id, student_id, grade, and teacher_id

### Requirement: Create API POST /activity_grades
The system SHALL provide an API endpoint to create new activity grades.

#### Scenario: Teacher submits grade via API
- **WHEN** teacher sends POST request to /activity_grades with activity_id, student_id, grade
- **THEN** system creates the grade record and returns success response

### Requirement: Create API GET /activity_grades
The system SHALL provide an API endpoint to retrieve activity grades assigned by the authenticated teacher.

#### Scenario: Teacher views assigned grades
- **WHEN** teacher sends GET request to /activity_grades
- **THEN** system returns list of grades assigned by the teacher