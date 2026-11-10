-- Dados fictícios. Empresa emissora simulada: UF = SP.

INSERT INTO customers (name, state) VALUES
 ('Comercial Alfa (fictício)',      'SP'),
 ('Distribuidora Beta (fictício)',  'RJ'),
 ('Indústria Gama (fictício)',      'SP'),
 ('Varejo Delta (fictício)',        'MG');

INSERT INTO materials (description, ncm) VALUES
 ('Parafuso de aço 10 mm', '73181500'),
 ('Chave de fenda',        '82054000'),
 ('Fita isolante',         '39191010'),
 ('Caixa plástica',        '39231090');

INSERT INTO sales_orders (customer_id, order_date, status, block_reason) VALUES
 (1, '2026-10-01', 'FATURADO',   NULL),                         -- 1: fluxo completo
 (2, '2026-10-02', 'FATURADO',   NULL),                         -- 2: fluxo completo
 (3, '2026-10-03', 'FATURADO',   NULL),                         -- 3: fluxo completo
 (1, '2026-10-05', 'ABERTO',     NULL),                         -- 4: sem remessa
 (4, '2026-10-06', 'EM_REMESSA', NULL),                         -- 5: remessa sem fatura
 (2, '2026-10-07', 'FATURADO',   NULL),                         -- 6: fatura com valor divergente
 (3, '2026-10-08', 'FATURADO',   NULL),                         -- 7: NF-e rejeitada + CFOP incompatível
 (1, '2026-10-09', 'BLOQUEADO',  'Limite de crédito excedido'), -- 8: bloqueado
 (4, '2026-10-10', 'FATURADO',   NULL),                         -- 9: NF-e pendente
 (2, '2026-10-12', 'ABERTO',     NULL);                         -- 10: recente, ainda dentro do prazo

INSERT INTO order_items (order_id, material_id, quantity, unit_price, cfop) VALUES
 (1, 1, 10, 2.50, '5102'), (1, 2, 2, 15.00, '5102'),
 (2, 3, 5, 8.00, '6102'),
 (3, 4, 3, 20.00, '5102'), (3, 1, 20, 2.50, '5102'),
 (4, 2, 4, 15.00, '5102'),
 (5, 1, 100, 2.50, '6102'),
 (6, 4, 10, 20.00, '6102'),
 (7, 2, 6, 15.00, '5102'), (7, 3, 1, 8.00, '6102'),   -- CFOP 6102 para cliente de SP: erro proposital
 (8, 3, 50, 8.00, '5102'),
 (9, 1, 8, 2.50, '6102'),
 (10, 3, 2, 8.00, '6102');

INSERT INTO deliveries (order_id, delivery_date, status) VALUES
 (1, '2026-10-02', 'ENTREGUE'),
 (2, '2026-10-03', 'ENTREGUE'),
 (3, '2026-10-04', 'ENTREGUE'),
 (5, '2026-10-08', 'EM_TRANSITO'),
 (6, '2026-10-08', 'ENTREGUE'),
 (7, '2026-10-09', 'ENTREGUE'),
 (9, '2026-10-11', 'ENTREGUE');

INSERT INTO invoices (order_id, delivery_id, invoice_date, total_value, nfe_status, rejection_code, rejection_reason) VALUES
 (1, 1, '2026-10-02',  55.00, 'AUTORIZADA', NULL,  NULL),
 (2, 2, '2026-10-03',  40.00, 'AUTORIZADA', NULL,  NULL),
 (3, 3, '2026-10-04', 110.00, 'AUTORIZADA', NULL,  NULL),
 (6, 5, '2026-10-08', 190.00, 'AUTORIZADA', NULL,  NULL),                 -- pedido soma 200,00
 (7, 6, '2026-10-09',  98.00, 'REJEITADA',  '778', 'NCM inexistente'),
 (9, 7, '2026-10-11',  20.00, 'PENDENTE',   NULL,  NULL);
