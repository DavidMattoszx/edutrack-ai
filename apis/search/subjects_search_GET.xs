// Hybrid search for subjects by name or overdue tasks
query "subjects/search" verb=GET {
  api_group = "search"
  auth = "user"

  input {
    text query? filters=trim|lower
    text overdue? filters=trim|lower
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id && $db.subjects.archived == false
      return = {type: "list"}
    } as $subjects

    array.map ($subjects) {
      by = $this.id
    } as $user_subject_ids

    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.due_date < now && $db.academic_tasks.status != "concluida"
      return = {type: "list"}
    } as $overdue_tasks

    array.filter $overdue_tasks if ($user_subject_ids contains $this.subject_id) as $user_overdue_tasks

    array.map ($user_overdue_tasks) {
      by = $this.subject_id
    } as $overdue_subject_ids

    var $unique_overdue_subject_ids {
      value = $overdue_subject_ids|unique
    }

    var $filtered_subjects {
      value = $subjects
    }

    conditional {
      if (`$input.query != null && $input.query != ""`) {
        array.filter $filtered_subjects if (`$this.name|to_lower|contains:$input.query`) as $filtered_subjects
      }
      if (`$input.overdue != null && $input.overdue != "" && ($input.overdue == "true" || $input.overdue == "1" || $input.overdue == "yes")`) {
        array.filter $filtered_subjects if (`$unique_overdue_subject_ids contains $this.id`) as $filtered_subjects
      }
    }
  }

  response = {
    subjects: $filtered_subjects,
    overdue_subject_ids: $unique_overdue_subject_ids
  }
}
