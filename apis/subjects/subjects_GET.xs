// List all subjects owned by the authenticated user
query subjects verb=GET {
  api_group = "subjects"
  auth = "user"

  input {
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id && $db.subjects.archived == false
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
}
