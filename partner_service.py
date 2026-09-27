from database import get_connection
from partner_discount import calculate_partner_discount

def get_partner_with_discount(partner_id: int) -> dict:
    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                p.id,
                p.name,
                COALESCE(SUM(sh.quantity), 0) AS total_quantity
            FROM partners AS p
            LEFT JOIN sales_history AS sh
                ON sh.partner_id = p.id
            WHERE p.id = ?
            GROUP BY p.id, p.name
        """

        cursor.execute(query, (partner_id,))
        row = cursor.fetchone()

        if row is None:
            return {}

        total_quantity = row[2]
        discount = calculate_partner_discount(total_quantity)

        return {
            "id": row[0],
            "name": row[1],
            "total_quantity": total_quantity,
            "discount": discount,
        }
    finally:
        connection.close()

def get_all_partners_with_discount() -> list:
    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                p.id,
                p.name,
                COALESCE(SUM(sh.quantity), 0) AS total_quantity
            FROM partners AS p
            LEFT JOIN sales_history AS sh
                ON sh.partner_id = p.id
            GROUP BY p.id, p.name
            ORDER BY p.id
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        partners = []

        for row in rows:
            total_quantity = row[2]
            discount = calculate_partner_discount(total_quantity)

            partner = {
                "id": row[0],
                "name": row[1],
                "total_quantity": total_quantity,
                "discount": discount,
            }

            partners.append(partner)

        return partners
    finally:
        connection.close()


def get_partner_by_id(partner_id: int) -> dict:
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                inn,
                email,
                phone,
                rating,
                partner_type,
                address,
                director
            FROM partners
            WHERE id = ?
            """,
            (partner_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return {}

        return {
            "id": row[0],
            "name": row[1],
            "inn": row[2],
            "email": row[3],
            "phone": row[4],
            "rating": row[5],
            "partner_type": row[6],
            "address": row[7],
            "director": row[8],
        }
    finally:
        connection.close()


def create_partner(data: dict) -> int:
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO partners (
                name,
                inn,
                email,
                phone,
                rating,
                partner_type,
                address,
                director
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["inn"],
                data["email"],
                data["phone"],
                data["rating"],
                data["partner_type"],
                data["address"],
                data["director"],
            ),
        )

        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def update_partner(partner_id: int, data: dict) -> bool:
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Работаем по ID, чтобы изменение названия партнера не нарушало связи.
        cursor.execute(
            """
            UPDATE partners
            SET
                name = ?,
                inn = ?,
                email = ?,
                phone = ?,
                rating = ?,
                partner_type = ?,
                address = ?,
                director = ?
            WHERE id = ?
            """,
            (
                data["name"],
                data["inn"],
                data["email"],
                data["phone"],
                data["rating"],
                data["partner_type"],
                data["address"],
                data["director"],
                partner_id,
            ),
        )

        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()