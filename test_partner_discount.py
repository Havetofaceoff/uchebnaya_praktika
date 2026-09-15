import unittest

from partner_discount import calculate_partner_discount

class TestCalculatePartnerDiscount(unittest.TestCase):
    def test_9999(self):
        self.assertEqual(calculate_partner_discount(9_999), 0)

    def test_10000(self):
        self.assertEqual(calculate_partner_discount(10_000), 5)

    def test_49999(self):
        self.assertEqual(calculate_partner_discount(49_999), 5)

    def test_50000(self):
        self.assertEqual(calculate_partner_discount(50_000), 10)

    def test_300000(self):
        self.assertEqual(calculate_partner_discount(300_000), 15)

if __name__ == "__main__":
    unittest.main()