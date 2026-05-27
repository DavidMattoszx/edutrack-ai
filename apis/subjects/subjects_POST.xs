// Create a new subject for the authenticated user
query subjects verb=POST {
  api_group = "subjects"
  auth = "user"

  input {
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    var $subject_data {
      value = $raw_input|filter_null|filter_empty_text
    }

    var $subject_name {
      value = $subject_data|get:"name"
    }

    precondition ($subject_name != null && $subject_name != "") {
      error_type = "badrequest"
      error = "Subject name is required."
    }

    db.query subjects {
      where = $db.subjects.user_id == $auth.id && $db.subjects.name == $subject_name
      return = {type: "single"}
    } as $existing_subject

    precondition ($existing_subject == null) {
      error_type = "badrequest"
      error = "You already have a subject with this name."
    }

    db.add subjects {
      data = $subject_data|set:"user_id":$auth.id|set:"archived":false
    } as $subjects
  }

  response = $subjects
}
