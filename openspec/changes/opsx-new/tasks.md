# EduTrack AI Full System Tasks

- [x] Define JWT authentication flow with signup, login, session persistence, token expiration, and token validation.
- [x] Create user profile management endpoints to update name and email securely.
- [x] Implement password reset and change-password functionality for authenticated users.
- [x] Add secure `subjects` CRUD endpoints scoped to the authenticated user.
- [x] Add validation to prevent duplicate subject names for the same user.
- [x] Add hybrid subject search endpoint supporting partial name search and overdue-task filtering.
- [x] Implement `academic_tasks` CRUD endpoints with task association to subject and authenticated user.
- [x] Add task status filters for Pendente, Em andamento, Concluída and overdue detection when `due_date < now`.
- [x] Add task completion toggling and task grouping by subject and deadline.
- [x] Implement task priority field with values Baixa, Média, Alta.
- [x] Add discipline archiving support for completed subjects and subject visibility rules.
- [x] Create Streamlit dashboard views for summary metrics, upcoming tasks, progress bar, and active subjects.
- [x] Build Streamlit reports view with historical task filtering and CSV export.
- [x] Add confirmation UI patterns for deletes and archiving actions.
- [x] Ensure all API queries and mutations enforce `$auth.id` ownership checks and do not expose other users' data.
