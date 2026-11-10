# Runbook 02 — Pedido aberto sem remessa

**Sintoma:** o pedido de venda está aberto há dias e não gerou remessa.

**Impacto:** atraso na entrega ao cliente e no faturamento.

## Causas prováveis
- Pedido bloqueado (crédito, cadastro ou fiscal).
- Falta de estoque ou de disponibilidade do material.
- Cadastro do cliente ou do material incompleto.
- Remessa ainda não criada pela logística.

## Como analisar
1. Rode a consulta Q1 para listar pedidos abertos sem remessa há mais de 3 dias.
2. Rode a consulta Q6 para ver se o pedido está bloqueado e qual o motivo.
3. Confira cliente, material e quantidades do pedido.
4. Verifique com a logística se há estoque.

## Como resolver
- Bloqueio de crédito: encaminhar ao financeiro ou ao responsável pela liberação.
- Falta de estoque: informar a previsão ao cliente e ao comercial.
- Cadastro incompleto: corrigir com a área dona do dado.

## Quando escalar
- Pedido parado sem causa clara após as verificações acima.
- Impacto em cliente crítico ou prazo contratual.

## Evidências para anexar
Número do pedido, data de criação, status, motivo de bloqueio (se houver) e resultado das consultas Q1 e Q6.
