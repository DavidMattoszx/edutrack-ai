# api-crud-subjects Tasks

- [ ] Create `POST /subjects` endpoint to add a new subject for the authenticated user
- [ ] Create `GET /subjects` endpoint to list subjects owned by the authenticated user
- [ ] Create `PATCH /subjects/{id}` endpoint to update a subject only if it belongs to the authenticated user
- [ ] Create `DELETE /subjects/{id}` endpoint to remove a subject only if it belongs to the authenticated user
- [ ] Enforce security by filtering all queries and mutations with `user_id == auth.id`