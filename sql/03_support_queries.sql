-- Consultas de investigação usadas no suporte N1/Júnior.
-- Data de referência fixa para o laboratório: 2026-10-13.

-- Q1. Pedidos abertos sem remessa há mais de 3 dias (e não bloqueados)
SELECT o.order_id, c.name AS cliente, o.order_date,
       ('2026-10-13'::date - o.order_date) AS dias_parado
FROM sales_orders o
JOIN customers c ON c.customer_id = o.customer_id
LEFT JOIN deliveries d ON d.order_id = o.order_id
WHERE d.delivery_id IS NULL
  AND o.status = 'ABERTO'
  AND ('2026-10-13'::date - o.order_date) > 3
ORDER BY dias_parado DESC;

-- Q2. Remessas sem faturamento
SELECT d.delivery_id, d.order_id, d.delivery_date, d.status
FROM deliveries d
LEFT JOIN invoices i ON i.delivery_id = d.delivery_id
WHERE i.invoice_id IS NULL;

-- Q3. Valor da fatura diferente do total do pedido
SELECT i.invoice_id, i.order_id, t.order_total, i.total_value,
       (i.total_value - t.order_total) AS diferenca
FROM invoices i
JOIN v_order_totals t ON t.order_id = i.order_id
WHERE i.total_value <> t.order_total;

-- Q4. NF-e rejeitadas ou pendentes de autorização
SELECT i.invoice_id, i.order_id, i.nfe_status, i.rejection_code, i.rejection_reason
FROM invoices i
WHERE i.nfe_status IN ('REJEITADA','PENDENTE')
ORDER BY i.nfe_status, i.invoice_id;

-- Q5. CFOP incompatível com a UF do cliente (emissor simulado em SP)
--     5xxx = operação dentro do estado | 6xxx = operação interestadual
SELECT o.order_id, c.name AS cliente, c.state AS uf_cliente, i.cfop
FROM order_items i
JOIN sales_orders o ON o.order_id = i.order_id
JOIN customers c    ON c.customer_id = o.customer_id
WHERE (c.state = 'SP' AND LEFT(i.cfop, 1) <> '5')
   OR (c.state <> 'SP' AND LEFT(i.cfop, 1) <> '6');

-- Q6. Pedidos bloqueados e motivo
SELECT order_id, order_date, block_reason
FROM sales_orders
WHERE status = 'BLOQUEADO';
