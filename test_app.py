import unittest
from app import calculate_bmr, calculate_calories, classify_bmi

class TestFitBiteFunctions(unittest.TestCase):

    def test_calculate_bmr_male(self):
        self.assertAlmostEqual(calculate_bmr(25, 180, 70, "Male"), 1705.0)

    def test_calculate_bmr_female(self):
        self.assertAlmostEqual(calculate_bmr(25, 160, 55, "Female"), 1264.0)


    def test_calculate_calories_sedentary(self):
        bmr = 1500
        self.assertEqual(calculate_calories(bmr, "Sedentary"), 1800.0)

    def test_calculate_calories_very_active(self):
        bmr = 1500
        self.assertEqual(calculate_calories(bmr, "Very active"), 2587.5)

    def test_classify_bmi_underweight(self):
        self.assertEqual(classify_bmi(17.5), "Underweight")

    def test_classify_bmi_healthy(self):
        self.assertEqual(classify_bmi(22), "Healthy Weight")

    def test_classify_bmi_overweight(self):
        self.assertEqual(classify_bmi(27), "Overweight")

    def test_classify_bmi_obese(self):
        self.assertEqual(classify_bmi(31), "Obese")

if __name__ == '__main__':
    unittest.main()
