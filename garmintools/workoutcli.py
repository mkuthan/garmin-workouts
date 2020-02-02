import argparse
import glob

from config.config import read_config
from garmin.garminclient import GarminClient
from models.workout import build_cycling_workout, get_workout_name, get_workout_id


def main():
    parser = argparse.ArgumentParser(description='Import Garmin workout(s) from definition in YAML file')
    parser.add_argument("--configuration", required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--ftp', required=True, type=int)

    args = parser.parse_args()
    config_files = glob.glob(args.configuration)

    configs = [read_config(config_file) for config_file in config_files]
    workouts = [build_cycling_workout(config, args.ftp) for config in configs]

    with GarminClient(username=args.username, password=args.password) as connection:
        existing_workouts = connection.list_workouts()

        for workout in workouts:
            workout_name = get_workout_name(workout)
            workout_id = next(get_workout_id(existing_workout)
                              for existing_workout in existing_workouts
                              if get_workout_name(existing_workout) == get_workout_name(workout_name))

            if workout_id:
                print("Delete workout: %s (%s)" % (workout_name, workout_id))
                connection.delete_workout(workout_id)

            print("Save workout: %s" % workout_name)
            connection.save_workout(workout)


if __name__ == "__main__":
    main()
