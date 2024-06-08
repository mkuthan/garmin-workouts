from _pytest.capture import CaptureResult
import pytest
from garminworkouts.models.trainingplan import TrainingPlan

# Positive test cases


def test_extract_trainingplan_id() -> None:
    tp: dict[str, str] = {'id': '12345'}
    assert TrainingPlan.extract_trainingplan_id(tp) == '12345'


def test_extract_trainingplan_type() -> None:
    tp: dict[str, str] = {'type': 'Strength'}
    assert TrainingPlan.extract_trainingplan_type(tp) == 'Strength'


def test_extract_trainingplan_level() -> None:
    tp: dict[str, str] = {'level': 'Beginner'}
    assert TrainingPlan.extract_trainingplan_level(tp) == 'Beginner'


def test_extract_trainingplan_version():
    tp: dict[str, str] = {'version': '1.0'}
    assert TrainingPlan.extract_trainingplan_version(tp) == '1.0'


def test_extract_trainingplan_name() -> None:
    tp: dict[str, str] = {'name': 'Weightlifting Plan'}
    assert TrainingPlan.extract_trainingplan_name(tp) == 'Weightlifting Plan'


def test_print_trainingplan_summary(capsys: pytest.CaptureFixture[str]) -> None:
    tp: dict[str, str] = {
        'id': '12345',
        'name': 'Weightlifting Plan',
        'type': 'Strength',
        'level': 'Beginner',
        'version': '1.0'}
    TrainingPlan.print_trainingplan_summary(tp)
    captured: CaptureResult[str] = capsys.readouterr()
    assert captured.out == "12345 Weightlifting Plan  Strength Beginner 1.0\n"


def test_export_trainingplan() -> None:
    tp: dict = {
        'trainingPlanId': '12345',
        'trainingType': {'typeKey': 'Strength'},
        'trainingSubType': {'subTypeKey': 'Weightlifting'},
        'trainingLevel': {'levelKey': 'Beginner'},
        'trainingVersion': {'versionName': '1.0'},
        'name': 'Weightlifting Plan',
        'description': 'This plan focuses on strength training',
        'durationInWeeks': 12,
        'avgWeeklyWorkouts': 4
    }
    expected_output: dict = {
        'id': '12345',
        'type': 'Strength',
        'subtype': 'Weightlifting',
        'level': 'Beginner',
        'version': '1.0',
        'name': 'Weightlifting Plan',
        'description': 'This plan focuses on strength training',
        'durationInWeeks': 12,
        'avgWeeklyWorkouts': 4
    }
    assert TrainingPlan.export_trainingplan(tp) == expected_output

# Negative test cases


def test_extract_trainingplan_id_missing_key() -> None:
    tp: dict = {}
    with pytest.raises(KeyError):
        TrainingPlan.extract_trainingplan_id(tp)


def test_extract_trainingplan_type_missing_key() -> None:
    tp: dict = {}
    with pytest.raises(KeyError):
        TrainingPlan.extract_trainingplan_type(tp)

# Add more negative test cases as needed
