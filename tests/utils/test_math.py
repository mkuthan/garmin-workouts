import unittest

import numpy as np

from garminworkouts.utils import math


class MathTestCase(unittest.TestCase):
    @staticmethod
    def test_moving_average():
        x = np.concatenate((np.full(5, 1), np.full(5, 2), np.full(5, 1)))
        y = math.moving_average(x, 5)
        expected = [1, 1.2, 1.4, 1.6, 1.8, 2, 1.8, 1.6, 1.4, 1.2, 1]
        np.testing.assert_array_almost_equal(y, expected)

    def test_normalized_power(self):
        x = np.concatenate((np.full(300, 150), np.full(300, 200), np.full(300, 150)))
        y = math.normalized_power(x)
        expected = 172
        self.assertAlmostEqual(y, expected, delta=0.5)

    def test_intensity_factory(self):
        norm_pwr = 150
        ftp = 200
        self.assertEqual(math.intensity_factor(norm_pwr, ftp), 0.75)

    def test_training_stress_score(self):
        seconds = 3600
        norm_pwr = 200
        ftp = 200
        self.assertEqual(math.training_stress_score(seconds, norm_pwr, ftp), 100)


if __name__ == "__main__":
    unittest.main()
