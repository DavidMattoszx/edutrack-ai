# api-crud-subjects Proposal

## Why
The system needs secure REST APIs for managing subjects so that the frontend can create, read, update, and delete subjects while respecting user ownership.

## What Changes
- Add CRUD endpoints for the `subjects` table:
  - `POST /subjects`
  - `GET /subjects`
  - `PATCH /subjects/{id}`
  - `DELETE /subjects/{id}`
- Enforce authorization so each user only accesses and modifies their own subject records.
- Use the authenticated user's `id` in all data queries and mutations.

## Impact
This change enables the Streamlit frontend to manage subject records securely and ensures that users cannot view or change other users' subjects.