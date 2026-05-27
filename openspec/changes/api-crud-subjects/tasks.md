# api-crud-subjects Tasks

- [x] Create `POST /subjects` endpoint to add a new subject for the authenticated user
- [x] Create `GET /subjects` endpoint to list subjects owned by the authenticated user
- [x] Create `PATCH /subjects/{id}` endpoint to update a subject only if it belongs to the authenticated user
- [x] Create `DELETE /subjects/{id}` endpoint to remove a subject only if it belongs to the authenticated user
- [x] Enforce security by filtering all queries and mutations with `user_id == auth.id`