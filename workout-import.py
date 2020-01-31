import argparse

from configreader import ConfigReader
from garminclient import GarminClient


def main():
    parser = argparse.ArgumentParser(description='Import Garmin workout from definition in YAML file')
    parser.add_argument("--configuration", required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)

    args = parser.parse_args()

    configuration = ConfigReader(args.configuration).read()
    print(configuration)

    # with GarminClient(username=args.username, password=args.password) as connection:
    #     workouts = connection.list_workouts()
    #     print(workouts)
    #
    #     workout = connection.get_workout("176144123")
    #     print(workout)


if __name__ == "__main__":
    main()
