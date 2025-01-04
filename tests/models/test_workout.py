import unittest
from datetime import date, timedelta
from unittest.mock import patch
import account
import logging
import os
from garminworkouts.models.fields import _STEPS
from garminworkouts.models.workout import Workout
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from garminworkouts.config import configreader
import math


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

    def test_print_workout_summary(self) -> None:
        workout: dict = {
            'workoutId': '123',
            'workoutName': 'Test Workout',
            'description': 'This is a test workout'
        }

        expected_output = '123 Test Workout         This is a test workout'

        with patch('builtins.print') as mock_print:
            Workout.print_workout_summary(workout)
            mock_print.assert_called_once_with(expected_output)

    def test_extract_workout_author(self) -> None:
        workout: dict = {
            'author': {
                'name': 'John Doe',
                'email': 'johndoe@example.com'
            }
        }

        expected_author: dict = {
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        author: dict = Workout.extract_workout_author(workout)

        self.assertEqual(author, expected_author)

    def test_extract_workout_author_no_author(self) -> None:
        workout: dict = {}

        author: dict = Workout.extract_workout_author(workout)

        self.assertIsNone(author)

    def test_extract_workout_author_missing_name(self) -> None:
        workout: dict = {
            'author': {
                'email': 'johndoe@example.com'
            }
        }

        expected_author: dict = {
            'email': 'johndoe@example.com'
        }

        author: dict = Workout.extract_workout_author(workout)

        self.assertEqual(author, expected_author)

    def test_extract_workout_author_missing_email(self) -> None:
        workout: dict = {
            'author': {
                'name': 'John Doe'
            }
        }

        expected_author: dict = {
            'name': 'John Doe'
        }

        author: dict = Workout.extract_workout_author(workout)

        self.assertEqual(author, expected_author)

    def test_create_workout(self) -> None:
        workout_file: str = os.path.join('.', 'workouts', 'cardio_training', 'ADVANCED', 'BBtO4iZ.yaml')
        config: dict = configreader.read_config(workout_file)
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

        workout_id = '123'
        workout_owner_id = '456'
        workout_author: dict = {
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        expected_workout: dict = {
            'workoutId': '123',
            'ownerId': '456',
            'workoutName': 'Tabata Alternating Lunges, Crunches, Burpees & Planks',
            'description': '. Plan: . ',
            'sportType': {'sportTypeId': 6, 'sportTypeKey': 'cardio_training'},
            'subSportType': None,
            'author': {'name': 'John Doe', 'email': 'johndoe@example.com'},
            'estimatedDurationInSecs': None,
            'estimatedDistanceInMeters': None,
            'avgTrainingSpeed': None,
            'workoutSegments': [
                {
                    'segmentOrder': 1,
                    'sportType': {'sportTypeId': 6, 'sportTypeKey': 'cardio_training'},
                    'workoutSteps': workout._steps(workout.config.get(_STEPS))
                    }
                ],
        }

        created_workout: dict = workout.create_workout(workout_id, workout_owner_id, workout_author)

        self.assertEqual(created_workout, expected_workout)

    def test_equivalent_pace_speed_zone(self) -> None:
        step: dict = {
            "target": {
                "type": "speed.zone",
                "min": 10,
                "max": 12
            }
        }
        expected_pace = 11.0

        pace: float = self.workout.equivalent_pace(step)

        self.assertEqual(pace, expected_pace)

    def test_equivalent_pace_pace_zone(self) -> None:
        step: dict = {
            "target": {
                "type": "pace.zone",
                "min": 5.0,
                "max": 5.0
            }
        }
        expected_pace = 5.0

        pace: float = self.workout.equivalent_pace(step)

        self.assertEqual(pace, expected_pace)

    def test_print_workout_json(self) -> None:
        workout = {
            'workoutId': '123',
            'workoutName': 'Test Workout',
            'description': 'This is a test workout'
        }

        expected_output = '{"workoutId": "123", "workoutName": "Test Workout", "description": "This is a test workout"}'

        with patch('builtins.print') as mock_print:
            Workout.print_workout_json(workout)
            mock_print.assert_called_once_with(expected_output)

    def test_extract_workout_owner_id(self) -> None:
        workout: dict = {
            'ownerId': '12345'
        }

        owner_id: str = Workout.extract_workout_owner_id(workout)

        self.assertEqual(owner_id, '12345')

    def test_running_workout_with_plan(self) -> None:
        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200'),
            cFTP=Power('200'),
            plan='5K Training Plan',
            race=date.today()
        )
        expected_description = "Plan: 5K Training Plan. "
        expected_description += "Estimated Duration: 0:50:00; 10.44 km. 4:47 min/km - 73.08% vVO2. rTSS: 45.0. "
        expected_description += "ECOs: 100.0. "

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_running_workout_without_plan(self) -> None:
        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        expected_description = 'W1-Short Run. Estimated Duration: 0:50:00; 10.44 km. 4:47 min/km - 73.08% vVO2. '
        expected_description += 'rTSS: 45.0. ECOs: 100.0. '

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_cycling_workout(self) -> None:
        workout_file: str = os.path.join('.', 'trainingplans', 'Cycling', 'Garmin', 'Crit', 'Advanced', 'Power',
                                         'RacePhase1Base', 'R1_3.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        expected_description = 'FTP 200, TSS 96, NP 195, IF 0.98'

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_swimming_workout(self) -> None:
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
        workout.mileage = 1.5
        expected_description = '. Plan: . '

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_cardio_workout(self) -> None:
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
        workout.ratio = 0.75
        workout.tss = 50
        expected_description = '. Plan: . '

        description: str | None = workout._generate_description()

        self.assertEqual(description, expected_description)

    def test_target_type(self) -> None:
        workout = Workout()
        step_config: dict = {
            "type": "interval",
            "target": {
                "type": "power.zone",
                "min": 100,
                "max": 200
            }
        }
        expected_target_type: dict = {'workoutTargetTypeId': 2, 'workoutTargetTypeKey': 'power.zone'}

        target_type: dict = workout._target_type(step_config)

        self.assertEqual(target_type, expected_target_type)

    def test_target_type_nodict(self) -> None:
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=[],
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        step_config: dict = {
            "type": "interval",
            "target": '40<AEROBIC_PACE'
        }
        expected_target_type: dict = {'workoutTargetTypeId': 6, 'workoutTargetTypeKey': 'pace.zone'}

        target_type: dict = workout._target_type(step_config)

        self.assertEqual(target_type, expected_target_type)

    def test_target_type_nointarget(self) -> None:
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=[],
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )
        step_config: dict = {
            "type": "interval",
            "target": '40<AEROBI_PACE'
        }
        expected_target_type: dict = {'workoutTargetTypeId': 1, 'workoutTargetTypeKey': 'no.target'}

        target_type: dict = workout._target_type(step_config)

        self.assertEqual(target_type, expected_target_type)

    def test_extract_target_value_heart_rate_zone(self) -> None:
        step: dict = {
            "type": "heart.rate.zone",
            "zone": 2
        }

        target_type, target_value = self.workout.extract_target_value(step, "max")

        self.assertEqual(target_type, "heart.rate.zone")
        self.assertEqual(target_value, "0.8")

    def test_extract_target_value_power_zone(self) -> None:
        step: dict = {
            "type": "power.zone",
            "zone": 3
        }

        target_type, target_value = self.workout.extract_target_value(step, "min")

        self.assertEqual(target_type, "power.zone")
        self.assertEqual(target_value, "0.9")

    def test_sec_greater_than_zero_running(self):
        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        target: dict = configreader.read_config(r'target.yaml')
        workout = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date.today()
        )

        expected_duration: dict = {
            'estimatedDurationInSecs': 3000,
            'estimatedDistanceInMeters': 10440.0,
            'avgTrainingSpeed': 3.48
            }

        self.assertEqual(workout.get_estimated_duration(), expected_duration)

    def test_load_metrics(self) -> None:
        # Create mock workouts
        target: dict = configreader.read_config(r'target.yaml')

        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_1.yaml')
        config: dict = configreader.read_config(workout_file)
        workout1 = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date(2024, 1, 1)
        )

        workout_file: str = os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1',
                                         '21_2.yaml')
        config: dict = configreader.read_config(workout_file)
        workout2 = Workout(
            config=config,
            target=target,
            vVO2=Pace('3:30'),
            fmin=44,
            fmax=183,
            flt=167,
            rFTP=Power('200w'),
            cFTP=Power('200w'),
            plan='',
            race=date(2024, 1, 1)
        )

        workouts = [workout2, workout1]

        # Call load_metrics
        mileage, duration, tss, ECOs, Rdist, Rdists, day_min, day_max = Workout.load_metrics(workouts)

        # Assert the results
        self.assertEqual(mileage[21], 14.44)
        self.assertEqual(duration[21], timedelta(seconds=4377))
        self.assertEqual(tss[21], 154278.0)
        self.assertEqual(ECOs[21], 123.0)
        self.assertEqual(Rdist, [1377, 3000, 0, 0, 0, 0, 0, 0])
        self.assertEqual(Rdists[21], [1377, 3000, 0, 0, 0, 0, 0, 0])
        self.assertEqual(day_min, date(2023, 8, 1))
        self.assertEqual(day_max, date(2023, 8, 2))

        with self.assertLogs(level=logging.INFO) as cm:
            Workout.load_metrics(workouts)

        log_messages = cm.output
        self.assertEqual(['INFO:root:From 2023-08-01 to 2023-08-02',
                          'INFO:root:Week 21: 14.44 km - Duration: 1:12:57 - ECOs: 123.0'], log_messages)


class TestCalculateP(unittest.TestCase):
    def setUp(self):
        self.workout = Workout(
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

    def test_calculate_p_no_recovery_or_rest(self):
        result = self.workout.calculate_p(100, 0, 0, 50, 50, 50, 2.0)
        self.assertEqual(result, 0.0)

    def test_calculate_p_maxIF_less_than_or_equal_to_3(self):
        result = self.workout.calculate_p(100, 50, 50, 50, 50, 50, 2.0)
        expected = (50 + 50) / (100 + 50 + 50 + 50 + 50 + 50) * 100
        self.assertAlmostEqual(result, expected)

    def test_calculate_p_maxIF_less_than_or_equal_to_5(self):
        result = self.workout.calculate_p(100, 50, 50, 50, 50, 50, 4.0)
        D = 100 / (50 + 50)
        expected = 20.204 * math.log(D) - 50.791
        self.assertAlmostEqual(result, expected)

    def test_calculate_p_maxIF_less_than_or_equal_to_9(self):
        result = self.workout.calculate_p(100, 50, 50, 50, 50, 50, 8.0)
        D = 100 / (50 + 50)
        expected = 40.257 * math.log(D) - 35.627
        self.assertAlmostEqual(result, expected)

    def test_calculate_p_maxIF_less_than_or_equal_to_15(self):
        result = self.workout.calculate_p(100, 50, 50, 50, 50, 50, 14.0)
        D = 100 / (50 + 50)
        expected = 37.085 * math.log(D) - 6.219
        self.assertAlmostEqual(result, expected)

    def test_calculate_p_maxIF_greater_than_15(self):
        result = self.workout.calculate_p(100, 50, 50, 50, 50, 50, 16.0)
        D = 100 / (50 + 50)
        expected = 89.204 * D - 270532
        self.assertAlmostEqual(result, expected)


class TestIntensityFactor(unittest.TestCase):
    def setUp(self):
        self.workout = Workout(
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

    def test_intensity_factor_below_0_5(self):
        v = 0.4
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 0.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 0, 0, 0, 0])

    def test_intensity_factor_R0(self):
        v = 0.6
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 1.0)
        self.assertEqual(Rdist, [100, 0, 0, 0, 0, 0, 0, 0])

    def test_intensity_factor_R1(self):
        v = 0.7
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 2.0)
        self.assertEqual(Rdist, [0, 100, 0, 0, 0, 0, 0, 0])

    def test_intensity_factor_R2(self):
        v = 0.8
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 3.0)
        self.assertEqual(Rdist, [0, 0, 100, 0, 0, 0, 0, 0])

    def test_intensity_factor_R3(self):
        v = 0.9
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 5.0)
        self.assertEqual(Rdist, [0, 0, 0, 100, 0, 0, 0, 0])

    def test_intensity_factor_R3_plus(self):
        v = 1.0
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 9.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 100, 0, 0, 0])

    def test_intensity_factor_R4(self):
        v = 1.1
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 15.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 0, 100, 0, 0])

    def test_intensity_factor_R5(self):
        v = 1.3
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 40.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 0, 0, 100, 0])

    def test_intensity_factor_R6(self):
        v = 1.6
        duration_secs = 100
        Rdist = [0] * 8
        c, Rdist = self.workout.intensity_factor(v, duration_secs, Rdist)
        self.assertEqual(c, 50.0)
        self.assertEqual(Rdist, [0, 0, 0, 0, 0, 0, 0, 100])
