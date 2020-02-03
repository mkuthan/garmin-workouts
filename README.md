Garmin CLI Tools
================

Command line tools for Garmin Connect.

# Installation

Install dependencies:
```shell script
$ pipenv install
```

Run shell:
```shell script
$ pipenv shell
```

# Usage

## Workouts

Import workouts into Garmin Connect from definition in [YAML](https://yaml.org) files: 
```shell script
$ ./garmintools/workoutcli.py -u [GARMIN_USERNAME] -p [GARMIN_PASSWORD] import --ftp [YOUR_FTP] workouts/*.yaml
```

Sample workout definition:
```yaml
name: "A SS 4x9"
description: "9 min @ 90%, 3 min @ 60%"

steps:
  - !include inc/warmup-short.yaml
  - &INTERVAL
    - { power: 90, duration: "9:00", description: "go!" }
    - { power: 60, duration: "3:00", description: "slow down" }
  - *INTERVAL
  - *INTERVAL
  - !include inc/cooldown-default.yaml
```
* Thanks to YAML aliases, workout steps can be easily reused once defined.
* Common workout parts like warm-up or cool-down can be reused using custom ```!include``` YAML directive.
* Target power is defined as percent of FTP (provided as mandatory command line parameter).
If the target power is not specified "No target" will be used for the workout step.
* Duration is defined as MM:SS format. 
If the duration is not specified "Lap Button Press" will be used to move into next workout step.