-- Laboratório Order-to-Cash (simulação educacional, NÃO é SAP)
-- Todos os dados são fictícios.

DROP VIEW  IF EXISTS v_order_totals;
DROP TABLE IF EXISTS invoices, deliveries, order_items, sales_orders, materials, customers CASCADE;

CREATE TABLE customers (
    customer_id  SERIAL PRIMARY KEY,
    name         TEXT    NOT NULL,
    state        CHAR(2) NOT NULL              -- UF do cliente
);

CREATE TABLE materials (
    material_id  SERIAL PRIMARY KEY,
    description  TEXT    NOT NULL,
    ncm          CHAR(8) NOT NULL              -- classificação fiscal (8 dígitos)
);

CREATE TABLE sales_orders (
    order_id     SERIAL PRIMARY KEY,
    customer_id  INT  NOT NULL REFERENCES customers(customer_id),
    order_date   DATE NOT NULL,
    status       TEXT NOT NULL CHECK (status IN ('ABERTO','BLOQUEADO','EM_REMESSA','FATURADO')),
    block_reason TEXT
);

CREATE TABLE order_items (
    item_id      SERIAL PRIMARY KEY,
    order_id     INT           NOT NULL REFERENCES sales_orders(order_id),
    material_id  INT           NOT NULL REFERENCES materials(material_id),
    quantity     NUMERIC(12,3) NOT NULL CHECK (quantity > 0),
    unit_price   NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    cfop         CHAR(4)       NOT NULL
);

CREATE TABLE deliveries (
    delivery_id    SERIAL PRIMARY KEY,
    order_id       INT  NOT NULL REFERENCES sales_orders(order_id),
    delivery_date  DATE NOT NULL,
    status         TEXT NOT NULL CHECK (status IN ('EM_TRANSITO','ENTREGUE'))
);

CREATE TABLE invoices (
    invoice_id        SERIAL PRIMARY KEY,
    order_id          INT  NOT NULL REFERENCES sales_orders(order_id),
    delivery_id       INT  NOT NULL REFERENCES deliveries(delivery_id),
    invoice_date      DATE NOT NULL,
    total_value       NUMERIC(12,2) NOT NULL,
    nfe_status        TEXT NOT NULL CHECK (nfe_status IN ('PENDENTE','AUTORIZADA','REJEITADA')),
    rejection_code    TEXT,
    rejection_reason  TEXT
);

-- Total de cada pedido (soma dos itens)
CREATE VIEW v_order_totals AS
SELECT o.order_id,
       SUM(i.quantity * i.unit_price)::NUMERIC(12,2) AS order_total
FROM sales_orders o
JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.order_id;
