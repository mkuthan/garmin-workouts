import unittest

from numpy.testing import assert_array_equal

from garmintools.utils import functional


class MyTestCase(unittest.TestCase):
    def test_flatten_empty(self):
        self.assertEqual(functional.flatten([]), [])

    def test_flatten_flat(self):
        self.assertEqual(functional.flatten([1, 2, 3]), [1, 2, 3])

    def test_flatten_nested(self):
        self.assertEqual(functional.flatten([1, [2], 3]), [1, 2, 3])

    def test_fill(self):
        assert_array_equal(functional.fill(10, 2), [10, 10])

    def test_concatenate(self):
        assert_array_equal(functional.concatenate([0, 1], [2, 3]), [0, 1, 2, 3])


if __name__ == '__main__':
    unittest.main()
