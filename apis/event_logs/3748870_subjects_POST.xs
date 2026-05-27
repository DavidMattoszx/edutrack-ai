// Add subjects record
query subjects verb=POST {
  api_group = "Event Logs"
  auth = "user"

  input {
    dblink {
      table = "subjects"
    }
  }

  stack {
    db.add subjects {
      data = {user_id: $auth.id}
    } as $subjects
  }

  response = $subjects
}