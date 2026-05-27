// Tabela para armazenar as tarefas acadêmicas dos alunos
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now
  
    // Título da tarefa acadêmica
    text title
  
    // Descrição detalhada da tarefa
    text description
  
    // Data de vencimento da tarefa
    timestamp due_date
  
    // Status atual da tarefa (ex: pendente, em_progresso, concluida)
    text status?=pendente

    // Prioridade da tarefa
    text priority?=media {
      description = "Task priority: baixa, media, or alta"
    }

    // Referência ao usuário proprietário da tarefa
    int user_id
  
    // Referência para a disciplina à qual a tarefa pertence
    int subject_id {
      table = "subjects"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "subject_id"}]}
    {type: "btree", field: [{name: "user_id"}]}
  ]
}