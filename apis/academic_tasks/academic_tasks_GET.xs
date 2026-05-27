// List academic tasks for the authenticated user
query academic_tasks verb=GET {
  api_group = "academic_tasks"
  auth = "user"

  input {
    int subject_id? filters=min:1
    text status? filters=trim|lower
    text priority? filters=trim|lower
  }

  stack {
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id
      return = {type: "list"}
    } as $tasks

    conditional {
      if ($input.subject_id != null) {
        array.filter $tasks if ($this.subject_id == $input.subject_id) as $tasks
      }
      if ($input.status != null && $input.status != "") {
        array.filter $tasks if ($this.status == $input.status) as $tasks
      }
      if ($input.priority != null && $input.priority != "") {
        array.filter $tasks if ($this.priority == $input.priority) as $tasks
      }
    }
  }

  response = $tasks
}
