// Update an academic task if it belongs to the authenticated user
query "academic_tasks/{academic_tasks_id}" verb=PATCH {
  api_group = "academic_tasks"
  auth = "user"

  input {
    int academic_tasks_id? filters=min:1
    text title?
    text description?
    timestamp due_date?
    text priority? filters=trim|lower
    text status? filters=trim|lower
    int subject_id? filters=min:1
  }

  stack {
    db.query academic_tasks {
      where = $db.academic_tasks.id == $input.academic_tasks_id && $db.academic_tasks.user_id == $auth.id
      return = {type: "single"}
    } as $task

    precondition ($task != null) {
      error_type = "notfound"
      error = "Task not found or does not belong to the authenticated user."
    }

    conditional {
      if ($input.subject_id != null) {
        db.query subjects {
          where = $db.subjects.id == $input.subject_id && $db.subjects.user_id == $auth.id
          return = {type: "single"}
        } as $subject

        precondition ($subject != null) {
          error_type = "notfound"
          error = "Target subject not found or does not belong to the authenticated user."
        }
      }
    }

    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
      data = {
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        priority   : $input.priority
        status     : $input.status
        subject_id : $input.subject_id
      }|filter_null|filter_empty_text
    } as $updated_task
  }

  response = $updated_task
}
