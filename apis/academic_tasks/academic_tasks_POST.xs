// Create a new academic task for the authenticated user's subject
query academic_tasks verb=POST {
  api_group = "academic_tasks"
  auth = "user"

  input {
    int subject_id filters=min:1
    text title filters=trim
    text description?
    timestamp due_date
    text priority?=media filters=trim|lower
    text status?=pendente filters=trim|lower
  }

  stack {
    precondition ($input.subject_id != null && $input.title != null && $input.title != "" && $input.due_date != null) {
      error_type = "badrequest"
      error = "subject_id, title, and due_date are required."
    }

    db.query subjects {
      where = $db.subjects.id == $input.subject_id && $db.subjects.user_id == $auth.id
      return = {type: "single"}
    } as $subject

    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found or does not belong to the authenticated user."
    }

    db.add academic_tasks {
      data = {
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
        priority   : $input.priority
        user_id    : $auth.id
      }
    } as $task
  }

  response = $task
}
