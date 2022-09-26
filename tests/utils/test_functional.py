import unittest

import numpy as np

from garminworkouts.utils import functional


class FunctionalTestCase(unittest.TestCase):
    def test_flatten_empty(self):
        self.assertEqual(functional.flatten([]), [])

    def test_flatten_flat(self):
        self.assertEqual(functional.flatten([1, 2, 3]), [1, 2, 3])

    def test_flatten_nested(self):
        self.assertEqual(functional.flatten([1, [2], 3]), [1, 2, 3])

    @staticmethod
    def test_fill():
        np.testing.assert_array_equal(functional.fill(10, 2), [10, 10])

    @staticmethod
    def test_concatenate():
        np.testing.assert_array_equal(functional.concatenate([0, 1], [2, 3]), [0, 1, 2, 3])

    def test_filter_empty_value_is_none(self):
        value = {"k1": "v1", "k2": None}
        self.assertEqual(functional.filter_empty(value), {"k1": "v1"})

    def test_filter_empty_value_is_empty_array(self):
        value = {"k1": "v1", "k2": []}
        self.assertEqual(functional.filter_empty(value), {"k1": "v1"})

    def test_filter_empty_value_is_empty_dict(self):
        value = {"k1": "v1", "k2": {}}
        self.assertEqual(functional.filter_empty(value), {"k1": "v1"})

    def test_filter_empty_nested_value_is_none(self):
        value = {"k1": "v1", "k2": {"k3": "v3", "k4": None}}
        self.assertEqual(functional.filter_empty(value), {"k1": "v1", "k2": {"k3": "v3"}})

    def test_filter_empty_nested_value_is_empty_array(self):
        value = {"k1": "v1", "k2": {"k3": "v3", "k4": []}}
        self.assertEqual(functional.filter_empty(value), {"k1": "v1", "k2": {"k3": "v3"}})

    def test_filter_empty_nested_value_is_empty_dict(self):
        value = {"k1": "v1", "k2": {"k3": "v3", "k4": []}}
        self.assertEqual(functional.filter_empty(value), {"k1": "v1", "k2": {"k3": "v3"}})


if __name__ == '__main__':
    unittest.main()
