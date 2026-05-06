// Create a new activity grade record
query "activity_grades" verb=POST {
  api_group = "Grades"
  auth = "user"

  input {
    int activity_id?
    int student_id?
    float grade?
  }

  stack {
    // Validate required inputs
    precondition ($input.activity_id != null && $input.student_id != null && $input.grade != null) {
      error_type = "badrequest"
      error = "Missing required fields: activity_id, student_id, grade"
    }

    // Insert the new grade record
    db.insert activity_grades {
      activity_id = $input.activity_id
      student_id = $input.student_id
      teacher_id = $auth.id
      grade = $input.grade
    } as $new_grade
  }

  response = $new_grade
}