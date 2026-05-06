# Proposta: Criação da Tabela de Tarefas Acadêmicas

## Why (Por quê)

Atualmente, a plataforma não possui um meio para que os alunos possam registrar e gerenciar suas atividades e obrigações acadêmicas, como lições de casa, trabalhos e provas. A criação de uma estrutura de dados para armazenar essas informações é o primeiro passo para implementar funcionalidades que ajudem o aluno em sua organização.

## What Changes (O que muda)

Esta proposta introduz a criação de uma nova tabela no banco de dados chamada `academic_tasks`. Esta tabela será responsável por armazenar os detalhes de cada tarefa acadêmica.

## Impact (Impacto)

- **Impacto em API:** Nenhum. Esta change apenas cria a estrutura da tabela. As APIs para interagir com ela serão definidas em propostas futuras.
- **Impacto no Banco de Dados:** Adição da nova tabela `academic_tasks`. Nenhum schema existente será modificado.
- **Impacto no Frontend:** Nenhum. As alterações visuais serão tratadas em outras tasks.
