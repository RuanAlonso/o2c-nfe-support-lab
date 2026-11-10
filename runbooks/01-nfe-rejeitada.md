# Runbook 01 — NF-e rejeitada

**Sintoma:** a nota fiscal aparece como rejeitada, com código e motivo, e o faturamento não é concluído.

**Impacto:** o cliente não recebe a nota, a mercadoria pode ficar retida e a receita não é reconhecida.

## Causas prováveis
| Código (exemplo) | Motivo típico | Onde olhar |
|---|---|---|
| 225 | Falha no schema do XML | Estrutura e campos obrigatórios do XML |
| 778 | NCM inexistente | Cadastro do material (NCM com 8 dígitos) |
| 204 | Duplicidade de NF-e | Se a nota já foi autorizada antes |

> Os códigos acima são exemplos. Confirme sempre na tabela oficial de rejeições da SEFAZ.

## Como analisar
1. Anote o número do pedido, da fatura, o código e o motivo da rejeição.
2. Rode a consulta Q4 (`sql/03_support_queries.sql`) para ver as notas rejeitadas e pendentes.
3. Se tiver o XML, rode o validador: `python -m nfe_validator.validator caminho/da/nota.xml`.
4. Confira NCM, CFOP, CST e totais da nota.

## Como resolver
- Dado de cadastro errado (ex.: NCM): corrigir no cadastro do material e reemitir.
- Erro de CFOP ou de imposto: encaminhar ao fiscal para a correção, sem alterar por conta própria.
- Duplicidade: confirmar a situação da nota original antes de qualquer nova emissão.

## Quando escalar
- Rejeição que se repete após correção do cadastro.
- Divergência de imposto ou regra fiscal (acionar o time Fiscal).
- Erro de schema ou de integração (acionar a Engenharia).

## Evidências para anexar no chamado
Número do pedido e da fatura, código e texto da rejeição, resultado da consulta Q4, saída do validador e passos já tentados.
