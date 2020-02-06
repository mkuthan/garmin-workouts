Garmin CLI Tools
================

Command line tools for Garmin Connect.

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
```

# Usage

First call to Garmin Connect takes some time to authenticate user. 
Once user is authenticated [cookie jar](https://docs.python.org/3/library/http.cookiejar.html) is created with session cookies for further calls.
It is required due to strict request limits for Garmin [SSO](https://en.wikipedia.org/wiki/Single_sign-on) service.
If you get Authentication 403 errors, just remove cookie jar file in the current directory to wipe out session cookies and force re-authentication.

## Workouts

### Import Workouts

Import workouts into Garmin Connect from definitions in [YAML](https://yaml.org) files.
If the workout of defined name already exist it will be updated:
 
```shell script
$ ./garmintools/workoutcli.py -u [GARMIN_USERNAME] -p [GARMIN_PASSWORD] import --ftp [YOUR_FTP] workouts/*.yaml
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
* Duration is defined as MM:SS format. 
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
First repeat for warmup, second repeat for main interval (repeated 3 times) and the last repeat for cooldown.


### Export Workouts

Export all workouts from Garmin Connect into local directory:
 
```shell script
$ ./garmintools/workoutcli.py -u [GARMIN_USERNAME] -p [GARMIN_PASSWORD] export /mnt/GARMIN/NewFiles
```
