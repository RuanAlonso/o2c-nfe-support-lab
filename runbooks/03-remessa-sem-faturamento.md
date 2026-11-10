# Runbook 03 — Remessa sem faturamento

**Sintoma:** a mercadoria foi enviada, mas não existe fatura nem NF-e para a remessa.

**Impacto:** mercadoria saindo sem nota, risco fiscal e receita não reconhecida.

## Causas prováveis
- Faturamento ainda não executado.
- Erro no processo de faturamento (dados fiscais ou de preço faltando).
- Remessa criada em condição que impede o faturamento.

## Como analisar
1. Rode a consulta Q2 para listar remessas sem fatura.
2. Confira o status da remessa e a data (em trânsito ou entregue).
3. Verifique pedido, preço e dados fiscais do cliente e do material.

## Como resolver
- Se faltou executar o faturamento: acionar a área responsável.
- Se há erro de dados: corrigir na origem e refazer o faturamento.

## Quando escalar
- Remessa já entregue e sem nota: tratar como prioridade e avisar o Fiscal.
- Erro persistente no faturamento: Engenharia ou time responsável pela configuração.

## Evidências para anexar
Número da remessa e do pedido, status e data, resultado da consulta Q2 e mensagens de erro, se houver.
