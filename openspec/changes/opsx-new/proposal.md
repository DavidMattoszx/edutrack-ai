# EduTrack AI Full System Proposal

## Why
EduTrack AI needs a complete authenticated academic tracking platform with secure subject and task management. This proposal captures the end-to-end backend and frontend scope so the Streamlit UI can support authenticated users, personal data isolation, task prioritization, and actionable dashboards.

## What Changes
- Implement full JWT-based authentication flow with signup, login, session persistence, token expiration, and password reset.
- Add profile edit capabilities for authenticated users, including secure updates to name and email.
- Build secure CRUD APIs for `subjects` and `academic_tasks`, enforcing ownership by `user_id == $auth.id`.
- Prevent duplicate subjects with the same name for the same authenticated user.
- Add hybrid subject search supporting partial name matching and overdue-task filtering.
- Implement task management features: create, read, update, delete, mark completion, status filters, overdue detection, and discipline associations.
- Add Streamlit dashboard screens to show active subjects, pending and overdue tasks, upcoming deadlines, progress metrics, archives, and CSV export.
- Apply confirmation flows for destructive actions and maintain a clean, user-centric interface.

## Impact
- Enables a secure EduTrack AI experience where each user only sees and edits their own data.
- Provides a unified academic workflow with subjects, tasks, deadlines, priorities and progress visibility.
- Prepares the backend for a complete Streamlit dashboard and reporting frontend.
- Establishes a scalable foundation for future enhancements like team sharing and advanced analytics.
