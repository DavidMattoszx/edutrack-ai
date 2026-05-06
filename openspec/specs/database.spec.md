# Database Specification

## Purpose
This document specifies the database schema for the EduTrack AI platform.

## ADDED Requirements

### Requirement: Create academic_tasks table
The system SHALL store academic task information including title, description, due date, status, and subject.

#### Scenario: A new academic task is created
- **WHEN** a new academic task is created
- **THEN** the system stores the task with a title, description, due_date, a default status of "pendente", and a subject_id.
