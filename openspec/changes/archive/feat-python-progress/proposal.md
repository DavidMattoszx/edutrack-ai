# Proposta: Implementar Script de Cálculo de Progresso em Python

## Why (Por quê)

Atualmente, não há uma forma automatizada de calcular o progresso das tarefas acadêmicas. Um script para calcular a porcentagem de tarefas concluídas é necessário para fornecer aos usuários uma visão clara de seu desempenho e avanço nas disciplinas.

## What Changes (O que muda)

Esta proposta introduz um novo script Python `scripts/calculate_progress.py`. O script irá:
- Receber o número de tarefas concluídas e o total de tarefas.
- Calcular a porcentagem de progresso.
- Tratar casos de divisão por zero quando não houver tarefas.
- Retornar o resultado em formato JSON.

## Impact (Impacto)

- **Impacto em API:** Nenhum. Este script é uma ferramenta de backend e não expõe uma API diretamente.
- **Impacto no Banco de Dados:** Nenhum. O script apenas lê dados que serão fornecidos a ele.
- **Impacto no Frontend:** Nenhum. O resultado do script poderá ser consumido pelo frontend no futuro, mas esta change não implementa a integração.
