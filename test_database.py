import unittest

from partner_service import get_partner_with_discount

class TestPartnerService(unittest.TestCase):
    def test_partner_one(self):
        result = get_partner_with_discount(1)

        self.assertEqual(result["total_quantity"], 11_000)
        self.assertEqual(result["discount"], 5)

    def test_partner_two(self):
        result = get_partner_with_discount(2)

        self.assertEqual(result["total_quantity"], 55_000)
        self.assertEqual(result["discount"], 10)

    def test_partner_three(self):
        result = get_partner_with_discount(3)

        self.assertEqual(result["total_quantity"], 350_000)
        self.assertEqual(result["discount"], 15)

    def test_partner_without_sales(self):
        result = get_partner_with_discount(4)

        self.assertEqual(result["total_quantity"], 0)
        self.assertEqual(result["discount"], 0)

if __name__ == "__main__":
    unittest.main()