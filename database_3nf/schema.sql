
DROP TABLE IF EXISTS sales_history;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS partners;


CREATE TABLE partners (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    inn VARCHAR(12) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20) NOT NULL,
    rating INT NOT NULL DEFAULT 0
);


CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    article VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0)
);


CREATE TABLE sales_history (
    id INTEGER PRIMARY KEY,
    partner_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    delivery_date DATE NOT NULL,

    CONSTRAINT fk_sales_partner
        FOREIGN KEY (partner_id)
        REFERENCES partners(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT
);