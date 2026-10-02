import unittest

from material_calculator import calculate_required_material


class TestMaterialCalculator(unittest.TestCase):

    def test_standard_calculation(self):
        result = calculate_required_material(
            2,
            2,
            10,
            2.0,
            3.0,
        )

        self.assertEqual(result, 95)

    def test_rounding_up(self):
        result = calculate_required_material(
            1,
            2,
            1,
            1.0,
            1.1,
        )

        self.assertEqual(result, 2)

    def test_invalid_type_id(self):
        result = calculate_required_material(
            999,
            2,
            10,
            2.0,
            3.0,
        )

        self.assertEqual(result, -1)

    def test_negative_parameter(self):
        result = calculate_required_material(
            1,
            1,
            10,
            -2.0,
            3.0,
        )

        self.assertEqual(result, -1)

    def test_zero_quantity(self):
        result = calculate_required_material(
            1,
            1,
            0,
            2.0,
            3.0,
        )

        self.assertEqual(result, -1)


if __name__ == "__main__":
    unittest.main()