// Update a subject record if it belongs to the authenticated user
query "subjects/{subjects_id}" verb=PATCH {
  api_group = "subjects"
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
    } as $subject

    precondition ($subject != null) {
      error_type = "notfound"
      error = "Not Found."
    }

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    var $new_name {
      value = $raw_input|get:"name"
    }

    conditional {
      if ($new_name != null && $new_name != "") {
        db.query subjects {
          where = $db.subjects.user_id == $auth.id && $db.subjects.name == $new_name && $db.subjects.id != $input.subjects_id
          return = {type: "single"}
        } as $duplicate_subject

        precondition ($duplicate_subject == null) {
          error_type = "badrequest"
          error = "Another subject with this name already exists."
        }
      }
    }

    db.patch subjects {
      field_name = "id"
      field_value = $input.subjects_id
      data = $raw_input|filter_null|filter_empty_text
    } as $subject
  }

  response = $subject
}
