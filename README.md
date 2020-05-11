Garmin Connect Workouts Tools
================

![Python application](https://github.com/mkuthan/garmin-workouts/workflows/Python%20application/badge.svg)

Command line tools for managing Garmin Connect workouts.

Features:

* Target power is set according to Your current FTP.
* All workouts under Your control stored as JSON files.
* Easy to understand workout format, see examples below.
* Workout parts like warm-up or cool-down are reusable.
* The most important parameters (TSS, IF, NP) embedded in workout description field.

# Installation

Requirements:
* Python 3.x ([doc](https://www.python.org/downloads/))

Install Pipenv ([doc](https://pipenv-fork.readthedocs.io/en/latest/install.html)):
```bash
$ pip install --user pipenv
```

Install dependencies:
```shell script
$ pipenv install
```

Run Pipenv shell:
```shell script
$ pipenv shell
garmin-workouts % 
```

# Usage

First call to Garmin Connect takes some time to authenticate user. 
Once user is authenticated [cookie jar](https://docs.python.org/3/library/http.cookiejar.html) is created with session cookies for further calls.
It is required due to strict request limits for Garmin [SSO](https://en.wikipedia.org/wiki/Single_sign-on) service.

## Import Workouts

Import workouts into Garmin Connect from definitions in [YAML](https://yaml.org) files.
If the workout already exists it will be updated:
 
```shell script
garmin-workouts % python3 -m garminworkouts -u [GARMIN_USERNAME] -p [GARMIN_PASSWORD] import --ftp [YOUR_FTP] workouts/*.yaml
```

Sample workout definition:
```yaml
name: "Boring as hell but simple workout"

steps:
  - { power: 50, duration: "10:00" }
  - { power: 70, duration: "20:00" }
  - { duration: "5:00" }
  - { power: 70, duration: "20:00" }
  - { power: 50 }
```

* Target power is defined as percent of FTP (provided as mandatory command line parameter).
If the target power is not specified "No target" will be used for the workout step.
* Target power may be defined as absolute value like: "150W", it could be useful in FTP ramp tests.
* Duration is defined as HH:MM:SS (or MM:SS, or SS) format. 
If the duration is not specified "Lap Button Press" will be used to move into next workout step.

Reusing workout definitions:

```yaml
name: "Boring as hell but simple workout"

steps:
  - !include inc/warmup.yaml
  - { power: 70, duration: "20:00" }
  - { duration: "5:00" }
  - { power: 70, duration: "20:00" }
  - !include inc/cooldown.yaml
```

* `!include` is a custom YAML directive for including another file as a part of the workout.

Reusing workout steps:
```yaml
name: "Boring as hell but simple workout"

steps:
  - !include inc/warmup.yaml
  - &INTERVAL { power: 70, duration: "20:00" }
  - { duration: "5:00" }
  - *INTERVAL
  - !include inc/cooldown.yaml
```

* Thanks to YAML aliases, workout steps can be easily reused once defined.

Sample Over-Under workout:

```yaml
name: "OverUnder 3x9"

steps:
  - !include inc/warmup.yaml
  - &INTERVAL
    - &UNDER { power: 95, duration: "2:00" }
    - &OVER { power: 105, duration: "1:00" }
    - *UNDER
    - *OVER
    - *UNDER
    - *OVER
    - { power: 50, duration: "3:00" }
  - *INTERVAL
  - *INTERVAL
  - !include inc/cooldown.yaml
```

* All nested sections are mapped as repeated steps in Garmin Connect.
First repeat for warmup, second repeat for main interval (repeated 3 times) and the last one for cooldown.


## Export Workouts

Export all workouts from Garmin Connect into local directory as FIT files.
This is the easiest way to synchronize all workouts with Garmin device:
 
```shell script
garmin-workouts % python3 -m garminworkouts -u [GARMIN_USERNAME] -p [GARMIN_PASSWORD] export /mnt/GARMIN/NewFiles
```

## List Workouts

Print summary for all workouts (workout identifier, workout name and description):

```shell script
garmin-workouts % python3 -m garminworkouts -u [GARMIN_USERNAME] -p [GARMIN_PASSWORD] list
188952654 VO2MAX 5x4           FTP 214, TSS 80, NP 205, IF 0.96
188952362 TEMPO 3x15           FTP 214, TSS 68, NP 172, IF 0.81
188952359 SS 3x12              FTP 214, TSS 65, NP 178, IF 0.83
188952356 VO2MAX 5x3           FTP 214, TSS 63, NP 202, IF 0.95
188952357 OU 3x9               FTP 214, TSS 62, NP 188, IF 0.88
188952354 SS 4x9               FTP 214, TSS 65, NP 178, IF 0.83
188952350 TEMPO 3x10           FTP 214, TSS 49, NP 169, IF 0.79
188952351 TEMPO 3x12           FTP 214, TSS 57, NP 171, IF 0.80
188952349 OU 3x6               FTP 214, TSS 47, NP 181, IF 0.85
188952348 SS 6x6               FTP 214, TSS 65, NP 178, IF 0.83
187538946 TD Tempo 3x15        None
127739603 FTP RAMP             FTP 214, TSS 62, NP 230, IF 1.08
```

## Get Workout

Print full workout definition (as JSON):

```shell script
garmin-workouts % python3 -m garminworkouts -u [GARMIN_USERNAME] -p [GARMIN_PASSWORD] get --id [WORKOUT_ID]
{"workoutId": 188952654, "ownerId": 2043461, "workoutName": "VO2MAX 5x4", "description": "FTP 214, TSS 80, NP 205, IF 0.96", "updatedDate": "2020-02-11T14:37:56.0", ...
```

## Delete Workout

Permanently delete workout from Garmin Connect:

```shell script
garmin-workouts % python3 -m garminworkouts -u [GARMIN_USERNAME] -p [GARMIN_PASSWORD] delete --id [WORKOUT_ID]
```
