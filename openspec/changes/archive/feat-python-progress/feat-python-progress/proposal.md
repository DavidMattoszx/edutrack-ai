# feat-python-progress Proposal

## Why
O objetivo desta mudança é introduzir um script Python que calcule a porcentagem de progresso com base em tarefas concluídas e total de tarefas, entregando o resultado em formato JSON.

## What Changes
- Adicionar um novo script em `scripts/calculate_progress.py`.
- Implementar cálculo de porcentagem de progresso.
- Tratar casos de divisão por zero quando o total de tarefas for 0.
- Retornar o resultado em JSON.

## Impact
Esta mudança adiciona uma utilidade simples de cálculo de progresso que pode ser usada por outras partes do sistema para representar o andamento de tarefas.
