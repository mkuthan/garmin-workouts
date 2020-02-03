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

Import workouts into Garmin Connect: 
```shell script
$ ./garmintools/workoutcli.py -u [GARMIN_USERNAME] -p [GARMIN_PASSWORD] import --ftp [YOUR_FTP] workouts/*.yaml
```
