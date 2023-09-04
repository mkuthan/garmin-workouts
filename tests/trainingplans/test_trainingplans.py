import unittest
import datetime
from garminworkouts.models.settings import settings


class Arg(object):
    def __init__(
        self,
        trainingplan
    ) -> None:
        self.trainingplan = trainingplan


class TrainingPlanTestCase(unittest.TestCase):
    def test_trainingplan_pfitzinger(self) -> None:
        tp_list: list[str] = [
            '.\\fitz*\\5k\\63km\\*.yaml',
            '.\\fitz*\\base\\72km\\*.yaml',
            '.\\fitz*\\base\\97km\\*.yaml',
            '.\\fitz*\\Half\\76km\\*.yaml',
            '.\\fitz*\\Half\\102km\\*.yaml',
            '.\\fitz*\\Marathon\\88km\\*\\*.yaml',
            '.\\fitz*\\Marathon\\113km\\*\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_napier(self) -> None:
        tp_list: list[str] = [
            '.\\napier*\\Half\\Advanced\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_5k(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Running\\5k\\Beginner\\Time\\*.yaml',
            '.\\trainingplans\\Running\\5k\\Beginner\\HeartRate\\*.yaml',
            '.\\trainingplans\\Running\\5k\\Intermediate\\Time\\*.yaml',
            '.\\trainingplans\\Running\\5k\\Intermediate\\HeartRate\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_10k(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Running\\10k\\Beginner\\Time\\*.yaml',
            '.\\trainingplans\\Running\\10k\\Beginner\\HeartRate\\*.yaml',
            '.\\trainingplans\\Running\\10k\\Intermediate\\Time\\*.yaml',
            '.\\trainingplans\\Running\\10k\\Intermediate\\HeartRate\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_halfmarathon(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Running\\HalfMarathon\\Beginner\\Time\\*.yaml',
            '.\\trainingplans\\Running\\HalfMarathon\\Beginner\\HeartRate\\*.yaml',
            '.\\trainingplans\\Running\\HalfMarathon\\Intermediate\\Time\\*.yaml',
            '.\\trainingplans\\Running\\HalfMarathon\\Intermediate\\HeartRate\\*.yaml',
            '.\\trainingplans\\Running\\HalfMarathon\\Advanced\\Time\\*.yaml',
            '.\\trainingplans\\Running\\HalfMarathon\\Advanced\\HeartRate\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_marathon(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Running\\Marathon\\Beginner\\Time\\*.yaml',
            '.\\trainingplans\\Running\\Marathon\\Beginner\\HeartRate\\*.yaml',
            '.\\trainingplans\\Running\\Marathon\\Intermediate\\Time\\*.yaml',
            '.\\trainingplans\\Running\\Marathon\\Intermediate\\HeartRate\\*.yaml',
            '.\\trainingplans\\Running\\Marathon\\Advanced\\Time\\*.yaml',
            '.\\trainingplans\\Running\\Marathon\\Advanced\\HeartRate\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_runningother(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Running\\RunningOther\\Beginner\\Time\\GettingStarted\\*.yaml',
            '.\\trainingplans\\Running\\RunningOther\\Beginner\\HeartRate\\GettingStarted\\*.yaml',
            '.\\trainingplans\\Running\\RunningOther\\Intermediate\\Time\\GettingStarted\\*.yaml',
            '.\\trainingplans\\Running\\RunningOther\\Intermediate\\HeartRate\\GettingStarted\\*.yaml',
            '.\\trainingplans\\Running\\RunningOther\\Beginner\\Time\\ImproveYourFitness\\*.yaml',
            '.\\trainingplans\\Running\\RunningOther\\Beginner\\HeartRate\\ImproveYourFitness\\*.yaml',
            '.\\trainingplans\\Running\\RunningOther\\Intermediate\\Time\\ImproveYourFitness\\*.yaml',
            '.\\trainingplans\\Running\\RunningOther\\Intermediate\\HeartRate\\ImproveYourFitness\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_triathlonolympic(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Triathlon\\Olympic\\Beginner\\Time\\*.yaml',
            '.\\trainingplans\\Triathlon\\Olympic\\Beginner\\HeartRate\\*.yaml',
            '.\\trainingplans\\Triathlon\\Olympic\\Intermediate\\Time\\*.yaml',
            '.\\trainingplans\\Triathlon\\Olympic\\Intermediate\\HeartRate\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_triathlonsprint(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Triathlon\\Sprint\\Beginner\\Time\\*.yaml',
            '.\\trainingplans\\Triathlon\\Sprint\\Beginner\\HeartRate\\*.yaml',
            '.\\trainingplans\\Triathlon\\Sprint\\Intermediate\\Time\\*.yaml',
            '.\\trainingplans\\Triathlon\\Sprint\\Intermediate\\HeartRate\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclingcrit(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Cycling\\Crit\\Advanced\\HeartRate\\RacePhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Advanced\\Power\\RacePhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Intermediate\\HeartRate\\RacePhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Intermediate\\Power\\RacePhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Advanced\\HeartRate\\RacePhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Advanced\\Power\\RacePhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Intermediate\\HeartRate\\RacePhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Intermediate\\Power\\RacePhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Advanced\\HeartRate\\RacePhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Advanced\\Power\\RacePhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Intermediate\\HeartRate\\RacePhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\Crit\\Intermediate\\Power\\RacePhase3Peak\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclingfullcentury(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Cycling\\FullCentury\\Advanced\\HeartRate\\CenturyPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Advanced\\Power\\CenturyPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Intermediate\\HeartRate\\CenturyPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Intermediate\\Power\\CenturyPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Advanced\\HeartRate\\CenturyPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Advanced\\Power\\CenturyPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Intermediate\\HeartRate\\CenturyPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Intermediate\\Power\\CenturyPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Advanced\\HeartRate\\CenturyPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Advanced\\Power\\CenturyPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Intermediate\\HeartRate\\CenturyPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\FullCentury\\Intermediate\\Power\\CenturyPhase3Peak\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclinggranfondo(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Cycling\\GranFondo\\Advanced\\HeartRate\\GranFondoPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Advanced\\Power\\GranFondoPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Intermediate\\HeartRate\\GranFondoPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Intermediate\\Power\\GranFondoPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Advanced\\HeartRate\\GranFondoPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Advanced\\Power\\GranFondoPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Intermediate\\HeartRate\\GranFondoPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Intermediate\\Power\\GranFondoPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Advanced\\HeartRate\\GranFondoPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Advanced\\Power\\GranFondoPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Intermediate\\HeartRate\\GranFondoPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\GranFondo\\Intermediate\\Power\\GranFondoPhase3Peak\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclinghalfcentury(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Cycling\\HalfCentury\\Beginner\\HeartRate\\MetricCenturyPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\HalfCentury\\Beginner\\Power\\MetricCenturyPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\HalfCentury\\Beginner\\HeartRate\\MetricCenturyPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\HalfCentury\\Beginner\\Power\\MetricCenturyPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\HalfCentury\\Beginner\\HeartRate\\MetricCenturyPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\HalfCentury\\Beginner\\Power\\MetricCenturyPhase3Peak\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclingMTB(self) -> None:
        tp_list: list[str] = [
            '.\\trainingplans\\Cycling\\MountainBiking\\Advanced\\HeartRate\\MTBPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Advanced\\Power\\MTBPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Intermediate\\HeartRate\\MTBPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Intermediate\\Power\\MTBPhase1Base\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Advanced\\HeartRate\\MTBPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Advanced\\Power\\MTBPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Intermediate\\HeartRate\\MTBPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Intermediate\\Power\\MTBPhase2Build\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Advanced\\HeartRate\\MTBPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Advanced\\Power\\MTBPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Intermediate\\HeartRate\\MTBPhase3Peak\\*.yaml',
            '.\\trainingplans\\Cycling\\MountainBiking\\Intermediate\\Power\\MTBPhase3Peak\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_workouts(self) -> None:
        tp_list: list[str] = [
            '.\\workouts\\cardio_training\\ADVANCED\\*.yaml',
            '.\\workouts\\cardio_training\\INTERMEDIATE\\*.yaml',
            '.\\workouts\\cardio_training\\BEGINNER\\*.yaml',
            '.\\workouts\\hiit\\ADVANCED\\*.yaml',
            '.\\workouts\\hiit\\INTERMEDIATE\\*.yaml',
            '.\\workouts\\hiit\\BEGINNER\\*.yaml',
            '.\\workouts\\pilates\\ADVANCED\\*.yaml',
            '.\\workouts\\pilates\\INTERMEDIATE\\*.yaml',
            '.\\workouts\\pilates\\BEGINNER\\*.yaml',
            '.\\workouts\\strength_training\\ADVANCED\\*.yaml',
            '.\\workouts\\strength_training\\INTERMEDIATE\\*.yaml',
            '.\\workouts\\strength_training\\BEGINNER\\*.yaml',
            '.\\workouts\\yoga\\INTERMEDIATE\\*.yaml',
            '.\\workouts\\yoga\\BEGINNER\\*.yaml',
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')


if __name__ == '__main__':
    unittest.main()
