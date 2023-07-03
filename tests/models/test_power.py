import unittest

from garminworkouts.models.power import Power


class PowerTestCase(unittest.TestCase):
    def test_valid_power_to_watts_conversion(self):
        ftp = 200
        valid_powers = [
            ("0", 0),
            ("0%", 0),
            ("10", 20),
            ("10%", 20),
            ("100", 200),
            ("100%", 200),
            ("120", 240),
            ("120%", 240),
            ("150", 300),
            ("150%", 300),
            ("0W", 0),
            ("0w", 0),
            ("100W", 100),
            ("100w", 100),
            ("1000W", 1000),
            ("1000w", 1000)
        ]

        for power, watts in valid_powers:
            with self.subTest(msg="Expected %d watts for '%s' (ftp=%s)" % (watts, power, ftp)):
                self.assertEqual(Power(power).to_watts(ftp), watts)

    def test_invalid_power_to_watts_conversion(self):
        ftp = 200
        invalid_powers = ["-1", "-1%", "2500", "2500%", "-1W", "5000W", "foo", "foo%", "fooW"]

        for power in invalid_powers:
            with self.subTest(msg="Expected ValueError for '%s" % power):
                with self.assertRaises(ValueError):
                    Power(power).to_watts(ftp)

    def test_power_to_watts_conversion_with_valid_ftp(self):
        power = "50"
        valid_ftps = [
            (0, 0),
            (100, 50),
            (250, 125),
            (999, 500)
        ]
        for ftp, watts in valid_ftps:
            with self.subTest(msg="Expected %d watts for ftp '%s' (power=%s)" % (watts, ftp, power)):
                self.assertEqual(Power(power).to_watts(ftp), watts)

    def test_power_to_watts_conversion_with_invalid_ftp(self):
        power = "100"
        invalid_ftps = [-1, 1000, "foo"]
        for ftp in invalid_ftps:
            with self.subTest(msg="Expected ValueError for '%s" % ftp):
                with self.assertRaises(ValueError):
                    Power(power).to_watts(ftp)


if __name__ == '__main__':
    unittest.main()
