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