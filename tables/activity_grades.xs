table activity_grades {
  auth = false

  schema {
    int id
    int activity_id
    int student_id
    int teacher_id
    decimal grade
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "activity_id"}]}
    {type: "btree", field: [{name: "student_id"}]}
    {type: "btree", field: [{name: "teacher_id"}]}
  ]
}
