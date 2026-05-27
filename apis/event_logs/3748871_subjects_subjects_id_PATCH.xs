// Edit subjects record
query "subjects/{subjects_id}" verb=PATCH {
  api_group = "Event Logs"
  auth = "user"

  input {
    int subjects_id? filters=min:1
    dblink {
      table = "subjects"
    }
  }

  stack {
    db.query subjects {
      where = $db.subjects.id == $input.subjects_id && $db.subjects.user_id == $auth.id
      return = {type: "single"}
    } as $subjects
  
    precondition ($subjects != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch subjects {
      field_name = "id"
      field_value = $input.subjects_id
      data = $raw_input|filter_null|filter_empty_text
    } as $subjects
  }

  response = $subjects
}