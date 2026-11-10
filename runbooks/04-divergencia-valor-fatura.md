# Runbook 04 — Valor da fatura diferente do pedido

**Sintoma:** o total da fatura não bate com o total do pedido de venda.

**Impacto:** cobrança incorreta ao cliente, risco fiscal e retrabalho contábil.

## Causas prováveis
- Desconto, frete ou imposto aplicado de forma diferente do pedido.
- Preço alterado depois da criação do pedido.
- Item faturado parcialmente.
- Erro de arredondamento ou de cálculo.

## Como analisar
1. Rode a consulta Q3 para comparar o total do pedido com o da fatura.
2. Compare item a item: quantidade, preço unitário e impostos.
3. Se a divergência estiver na NF-e, rode o validador no XML.

## Como resolver
- Divergência legítima (desconto ou frete combinados): documentar o motivo.
- Erro de cálculo ou preço: acionar o responsável para corrigir e, se necessário, emitir o documento de ajuste.

## Quando escalar
- Diferença sem explicação clara.
- Nota já autorizada com valor errado (é preciso tratar pelo Fiscal).

## Evidências para anexar
Números do pedido e da fatura, totais de cada um, diferença calculada e resultado da consulta Q3.
