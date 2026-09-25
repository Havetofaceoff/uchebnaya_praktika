SELECT
    p.id,
    p.name,
    p.inn,
    p.email,
    COUNT(d.id) AS delivery_count
FROM partners AS p
LEFT JOIN deliveries AS d
    ON d.partner_id = p.id
GROUP BY
    p.id,
    p.name,
    p.inn,
    p.email
ORDER BY p.name ASC;



BEGIN;

INSERT INTO partners (
    name,
    legal_address,
    phone,
    email,
    inn
)
VALUES (
    'ООО Новый партнер',
    'г. Санкт-Петербург, Невский проспект, 1',
    '+79990000000',
    'new_partner@example.com',
    '7812345678'
);

INSERT INTO deliveries (
    partner_id,
    product_id,
    quantity,
    delivery_date,
    unit_price
)
VALUES (
    last_insert_rowid(),
    1,
    10,
    '2026-09-25',
    1500.00
);

COMMIT;


SELECT
    d.id AS delivery_id,
    p.name AS partner_name,
    pr.name AS product_name,
    d.delivery_date,
    d.quantity,
    d.unit_price,
    d.quantity * d.unit_price AS total_amount
FROM deliveries AS d
JOIN partners AS p
    ON p.id = d.partner_id
JOIN products AS pr
    ON pr.id = d.product_id
WHERE d.partner_id = 1
  AND d.delivery_date BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY d.delivery_date ASC;