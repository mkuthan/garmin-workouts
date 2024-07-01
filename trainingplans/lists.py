import os

PfitzingerLists: list[str] = [
    os.path.join('trainingplans', 'Running', 'Pfitzinger', '5k', '63km', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', '5k', '111km', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', 'base', '72km', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', 'base', '97km', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', 'Half', '76km', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', 'Half', '102km', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', 'Marathon', '88km', '*', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', 'Marathon', '113km', '*', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', 'Marathon', '113km-12w', '*', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', 'Marathon', 'Mult-4w', '*', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Pfitzinger', 'Marathon', 'Mult-8w', '*', '*.yaml'),
]

NapierLists: list[str] = [
    os.path.join('trainingplans', 'Running', 'Napier', 'Marathon', 'Advanced', '*', '*.yaml'),
    os.path.join('trainingplans', 'Running', 'Napier', 'Half', 'Advanced', '*', '*.yaml'),
]

NikeLists: list[str] = [
    os.path.join('trainingplans', 'Running', 'Nike', 'Marathon', '*.yaml'),
]


Garmin5k: list[str] = [
    os.path.join('trainingplans', 'Running', '*', '5k', 'Beginner', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', '5k', 'Beginner', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', '5k', 'Intermediate', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', '5k', 'Intermediate', 'HeartRate', '*.yaml'),
]

Garmin10k: list[str] = [
    os.path.join('trainingplans', 'Running', '*', '10k', 'Beginner', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', '10k', 'Beginner', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', '10k', 'Intermediate', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', '10k', 'Intermediate', 'HeartRate', '*.yaml'),
]

GarminHalf: list[str] = [
    os.path.join('trainingplans', 'Running', '*', 'HalfMarathon', 'Beginner', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'HalfMarathon', 'Beginner', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'HalfMarathon', 'Intermediate', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'HalfMarathon', 'Intermediate', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'HalfMarathon', 'Advanced', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'HalfMarathon', 'Advanced', 'HeartRate', '*.yaml'),
]

GarminMarathon: list[str] = [
    os.path.join('trainingplans', 'Running', '*', 'Marathon', 'Beginner', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'Marathon', 'Beginner', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'Marathon', 'Intermediate', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'Marathon', 'Intermediate', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'Marathon', 'Advanced', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'Marathon', 'Advanced', 'HeartRate', '*.yaml'),
]

GarminRunningOther: list[str] = [
    os.path.join('trainingplans', 'Running', '*', 'GettingStarted', 'Beginner', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'GettingStarted', 'Beginner', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'GettingStarted', 'Intermediate', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'GettingStarted', 'Intermediate', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'ImproveYourFitness', 'Beginner', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'ImproveYourFitness', 'Beginner', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'ImproveYourFitness', 'Intermediate', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Running', '*', 'ImproveYourFitness', 'Intermediate', 'HeartRate', '*.yaml'),
]

TriathlonOlympic: list[str] = [
    os.path.join('trainingplans', 'Triathlon', 'Garmin', 'Olympic', 'Beginner', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Triathlon', 'Garmin', 'Olympic', 'Beginner', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Triathlon', 'Garmin', 'Olympic', 'Intermediate', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Triathlon', 'Garmin', 'Olympic', 'Intermediate', 'HeartRate', '*.yaml'),
]

TriathlonSprint: list[str] = [
    os.path.join('trainingplans', 'Triathlon', 'Garmin', 'Sprint', 'Beginner', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Triathlon', 'Garmin', 'Sprint', 'Beginner', 'HeartRate', '*.yaml'),
    os.path.join('trainingplans', 'Triathlon', 'Garmin', 'Sprint', 'Intermediate', 'Time', '*.yaml'),
    os.path.join('trainingplans', 'Triathlon', 'Garmin', 'Sprint', 'Intermediate', 'HeartRate', '*.yaml'),
]

CyclingRace: list[str] = [
    os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'HeartRate',
                 'RacePhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'Power',
                 'RacePhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'HeartRate',
                 'RacePhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'Power',
                 'RacePhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'HeartRate',
                 'RacePhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'Power',
                 'RacePhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'HeartRate',
                 'RacePhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'Power',
                 'RacePhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'HeartRate',
                 'RacePhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'Power',
                 'RacePhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'HeartRate',
                 'RacePhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'Power',
                 'RacePhase3Peak', '*.yaml'),
]

CyclingCentury: list[str] = [
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'HeartRate',
                 'CenturyPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'Power',
                 'CenturyPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'HeartRate',
                 'CenturyPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'Power',
                 'CenturyPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'HeartRate',
                 'CenturyPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'Power',
                 'CenturyPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'HeartRate',
                 'CenturyPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'Power',
                 'CenturyPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'HeartRate',
                 'CenturyPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'Power',
                 'CenturyPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'HeartRate',
                 'CenturyPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'Power',
                 'CenturyPhase3Peak', '*.yaml'),
]

CyclingGranFondo: list[str] = [
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'HeartRate',
                 'GranFondoPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'Power',
                 'GranFondoPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'HeartRate',
                 'GranFondoPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'Power',
                 'GranFondoPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'HeartRate',
                 'GranFondoPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'Power',
                 'GranFondoPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'HeartRate',
                 'GranFondoPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'Power',
                 'GranFondoPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'HeartRate',
                 'GranFondoPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'Power',
                 'GranFondoPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'HeartRate',
                 'GranFondoPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'Power',
                 'GranFondoPhase3Peak', '*.yaml'),
]

CyclingMetricCentury: list[str] = [
    os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'HeartRate',
                 'MetricCenturyPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'Power',
                 'MetricCenturyPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'HeartRate',
                 'MetricCenturyPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'Power',
                 'MetricCenturyPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'HeartRate',
                 'MetricCenturyPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'Power',
                 'MetricCenturyPhase3Peak', '*.yaml'),
]

CyclingMTB: list[str] = [
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'HeartRate',
                 'MTBPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'Power',
                 'MTBPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'HeartRate',
                 'MTBPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'Power',
                 'MTBPhase1Base', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'HeartRate',
                 'MTBPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'Power',
                 'MTBPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'HeartRate',
                 'MTBPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'Power',
                 'MTBPhase2Build', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'HeartRate',
                 'MTBPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'Power',
                 'MTBPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'HeartRate',
                 'MTBPhase3Peak', '*.yaml'),
    os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'Power',
                 'MTBPhase3Peak', '*.yaml'),
]

WorkoutsList: list[str] = [
    os.path.join('workouts', 'strength_training', 'ADVANCED', '*.yaml'),
    os.path.join('workouts', 'strength_training', 'INTERMEDIATE', '*.yaml'),
    os.path.join('workouts', 'strength_training', 'BEGINNER', '*.yaml'),
    os.path.join('workouts', 'cardio_training', 'ADVANCED', '*.yaml'),
    os.path.join('workouts', 'cardio_training', 'INTERMEDIATE', '*.yaml'),
    os.path.join('workouts', 'cardio_training', 'BEGINNER', '*.yaml'),
    os.path.join('workouts', 'hiit', 'ADVANCED', '*.yaml'),
    os.path.join('workouts', 'hiit', 'INTERMEDIATE', '*.yaml'),
    os.path.join('workouts', 'hiit', 'BEGINNER', '*.yaml'),
    os.path.join('workouts', 'pilates', 'ADVANCED', '*.yaml'),
    os.path.join('workouts', 'pilates', 'INTERMEDIATE', '*.yaml'),
    os.path.join('workouts', 'pilates', 'BEGINNER', '*.yaml'),
    os.path.join('workouts', 'yoga', 'INTERMEDIATE', '*.yaml'),
    os.path.join('workouts', 'yoga', 'BEGINNER', '*.yaml'),
]

DarebeeLists: list[str] = [
    os.path.join('trainingplans', 'Strength', 'Darebee', 'Challenges', '3-normal', '1-minute plank', '*.yaml'),
    os.path.join('trainingplans', 'Strength', 'Darebee', 'Challenges', '3-normal', 'first thing plank hold', '*.yaml'),
    os.path.join('trainingplans', 'Strength', 'Darebee', 'Challenges', '3-normal', 'the miner', '*.yaml'),
    os.path.join('trainingplans', 'Strength', 'Darebee', 'Programs', '12 weeks to 5k', '*.yaml'),
]
