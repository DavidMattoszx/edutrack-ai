table subjects {
  auth = false

  schema {
    int id
    int user_id
    text name
    bool archived?=false {
      description = "Marks whether the subject has been archived by the user"
    }
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}