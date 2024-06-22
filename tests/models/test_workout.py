import unittest
from datetime import date
import account
import logging
import os
from garminworkouts.models.workout import Workout
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from garminworkouts.config import configreader


class ZonesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.workout = Workout(
            config={},
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

    def test_null_workout(self) -> None:
        with self.assertRaises(ValueError):
            Workout(
                config={'name': 'name'},
                target=[],
                vVO2=Pace('3:30'),
                fmin=account.fmin,
                fmax=account.fmax,
                flt=account.flt,
                rFTP=Power('200'),
                cFTP=Power('200'),
                plan='',
                race=date.today()
            ).create_workout()

    def test_zones(self) -> None:
        expected_zones: list[float] = [0.46, 0.6, 0.7, 0.8,
                                       (account.flt - account.fmin) / (account.fmax-account.fmin),
                                       1.0, 1.1]
        expected_hr_zones: list[int] = [int(account.fmin + zone * (account.fmax-account.fmin))
                                        for zone in expected_zones]
        expected_data: list = [{
            "changeState": "CHANGED",
            "trainingMethod": "HR_RESERVE",
            "lactateThresholdHeartRateUsed": account.flt,
            "maxHeartRateUsed": account.fmax,
            "restingHrAutoUpdateUsed": False,
            "sport": "DEFAULT",
            "zone1Floor": expected_hr_zones[0],
            "zone2Floor": expected_hr_zones[1],
            "zone3Floor": expected_hr_zones[2],
            "zone4Floor": expected_hr_zones[3],
            "zone5Floor": expected_hr_zones[4]
        }]

        zones, hr_zones, data = Workout(
            [],
            [],
            account.vV02,
            account.fmin,
            account.fmax,
            account.flt,
            account.rFTP,
            account.cFTP,
            str(''),
            date.today()
        ).hr_zones()

        self.assertEqual(zones, expected_zones)
        self.assertEqual(hr_zones, expected_hr_zones)
        self.assertEqual(data, expected_data)

        with self.assertLogs(level=logging.INFO) as cm:
            self.workout.zones()

        log_messages: list[str] = cm.output
        self.assertIn('INFO:root:::Heart Rate Zones::', log_messages)
        self.assertIn(f"INFO:root:fmin: {self.workout.fmin} flt: "
                      f"{self.workout.flt} fmax: {self.workout.fmax}", log_messages)
        for i in range(len(expected_zones)):
            self.assertIn(f"INFO:root: Zone {i}: {expected_hr_zones[i]} - "
                          f"{expected_hr_zones[i + 1] if i + 1 < len(expected_hr_zones) else 'max'}", log_messages)

        zones, rpower_zones, cpower_zones, _ = Power.power_zones(self.workout.rFTP, self.workout.cFTP)
        self.assertIn('INFO:root:::Running Power Zones::', log_messages)
        for i in range(len(rpower_zones)):
            self.assertIn(f"INFO:root: Zone {i}: {rpower_zones[i]} - "
                          f"{rpower_zones[i + 1] if i + 1 < len(rpower_zones) else 'max'} w", log_messages)

        self.assertIn('INFO:root:::Cycling Power Zones::', log_messages)
        for i in range(len(cpower_zones)):
            self.assertIn(f"INFO:root: Zone {i}: {cpower_zones[i]} - "
                          f"{cpower_zones[i + 1] if i + 1 < len(cpower_zones) else 'max'} w", log_messages)

    def test_get_workout_name(self) -> None:
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()

        # Assert that the returned workout name is correct
        self.assertEqual(workout_name, "Tabata Alternating Lunges, Crunches, Burpees & Planks")

    def test_get_workout_name_short(self) -> None:
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['name'] = '0_1'
        config['description'] = ''
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()
        self.assertEqual(workout_name, '0_1')

    def test_get_workout_name_med(self) -> None:
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['name'] = '0_1'
        config['description'] = 'Description'
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='plan',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()
        self.assertEqual(workout_name, '0_1-Description')

    def test_get_workout_name_long(self) -> None:
        # Create a Workout instance with a specific configuration
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
        config['name'] = '0_1'
        config['description'] = 'Long description for a long workout name'
        workout = Workout(
            config=config,
            target=[],
            vVO2=Pace('3:30'),
            fmin=account.fmin,
            fmax=account.fmax,
            flt=account.flt,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_name method
        workout_name: str = workout.get_workout_name()
        self.assertEqual(workout_name, '0_1-Long')

    def test_get_workout_date(self) -> None:
        # Create a Workout instance with a specific configuration
        workout = Workout(
            config={},
            target=[],
            vVO2=Pace('5:00'),
            fmin=60,
            fmax=200,
            flt=185,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )

        # Call the get_workout_date method
        workout_date, week, day = workout.get_workout_date()

        # Assert that the returned workout date, fmin, and fmax are correct
        self.assertEqual(workout_date, date.today())
        self.assertEqual(week, 0)
        self.assertEqual(day, 0)


if __name__ == '__main__':
    unittest.main()
