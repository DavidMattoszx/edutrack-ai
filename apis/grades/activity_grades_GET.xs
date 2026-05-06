// Retrieve activity grades for the authenticated teacher
query "activity_grades" verb=GET {
  api_group = "Grades"
  auth = "user"

  input {
  }

  stack {
    // Query grades assigned by the authenticated teacher
    db.query activity_grades {
      where = $db.activity_grades.teacher_id == $auth.id
      return = {type: "list"}
    } as $grades
  }

  response = $grades
}