query activity_grades verb=POST {
  api_group = "grades"
  auth = "user"

  input {
    int activity_id
    int student_id
    decimal grade
  }

  stack {
    precondition ($input.activity_id == null || $input.student_id == null || $input.grade == null) {
      error_type = "badrequest"
      error = "Missing required fields: activity_id, student_id, grade"
    }

    db.add activity_grades {
      data = {
        activity_id: $input.activity_id
        student_id: $input.student_id
        teacher_id: $auth.id
        grade: $input.grade
      }
    } as $new_grade
  }

  response = $new_grade
}

