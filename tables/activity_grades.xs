table activity_grades {
  schema {
    int id
    int activity_id
    int student_id
    int teacher_id
    float grade
    timestamp created_at?=now
    timestamp updated_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
}