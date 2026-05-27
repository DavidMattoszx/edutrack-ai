// Delete an academic task if it belongs to the authenticated user
query "academic_tasks/{academic_tasks_id}" verb=DELETE {
  api_group = "academic_tasks"
  auth = "user"

  input {
    int academic_tasks_id? filters=min:1
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

    db.del academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    }
  }

  response = null
}
