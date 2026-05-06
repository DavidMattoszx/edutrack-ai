# Activity Grades Feature Proposal

## Why
Professores precisam lançar notas para alunos em atividades específicas para avaliar o desempenho acadêmico. Esta funcionalidade permite o registro dessas notas de forma estruturada no sistema EduTrack AI.

## What Changes
- Criar tabela `activity_grades` para armazenar notas de atividades
- Criar API POST `/activity_grades` para lançar notas
- Garantir que apenas professores possam lançar notas para suas atividades

## Impact
- Professores poderão registrar notas diretamente no sistema
- Alunos poderão visualizar suas notas (futuramente)
- Melhora o controle acadêmico e avaliação de desempenho