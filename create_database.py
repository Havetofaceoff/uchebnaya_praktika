import sqlite3

connection = sqlite3.connect("partner_db.sqlite3")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS partners (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_history (
        id INTEGER PRIMARY KEY,
        partner_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (partner_id) REFERENCES partners(id)
    )
""")

cursor.execute("DELETE FROM sales_history")
cursor.execute("DELETE FROM partners")

cursor.executemany(
    "INSERT INTO partners (id, name) VALUES (?, ?)",
    [
        (1, "ООО Ромашка"),
        (2, "ООО Василек"),
        (3, "ООО Лютик"),
        (4, "ООО Незабудка"),
    ],
)

cursor.executemany(
    "INSERT INTO sales_history (partner_id, quantity) VALUES (?, ?)",
    [
        (1, 5000),
        (1, 6000),
        (2, 25000),
        (2, 30000),
        (3, 150000),
        (3, 200000),
    ],
)

connection.commit()
connection.close()

print("База данных успешно создана.")