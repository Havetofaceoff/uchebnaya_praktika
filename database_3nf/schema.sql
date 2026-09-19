PRAGMA foreign_keys = ON;

CREATE TABLE partners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    inn TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    phone TEXT NOT NULL,
    rating INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    article TEXT NOT NULL UNIQUE,
    price REAL NOT NULL CHECK (price >= 0)
);

CREATE TABLE sales_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partner_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    delivery_date TEXT NOT NULL,

    FOREIGN KEY (partner_id)
        REFERENCES partners(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);