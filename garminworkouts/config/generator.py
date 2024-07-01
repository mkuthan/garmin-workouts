from garminworkouts.models.duration import Duration


def recovery_step_generator(duration, pace=False) -> dict:
    return step_generator(
        type='recovery',
        duration=duration,
        target='RECOVERY_PACE',
        description='Recovery pace') if pace else step_generator(
        type='recovery',
        duration=duration,
        target='RECOVERY_HEART_RATE',
        description='Recovery pace')


def aerobic_step_generator(duration, pace=False) -> dict:
    return step_generator(
        duration=duration,
        target='AEROBIC_PACE',
        description='Aerobic pace') if pace else step_generator(
        duration=duration,
        target='AEROBIC_HEART_RATE',
        description='Aerobic pace')


def lt_step_generator(target: str, duration, pace=False) -> dict:
    d, s = margin_generator(target)
    return step_generator(
        duration=duration,
        target=d + 'THRESHOLD_PACE',
        description=s + 'Threshold pace') if pace else step_generator(
        duration,
        target=d + 'THRESHOLD_HEART_RATE',
        description=s + 'Threshold pace')


def lr_step_generator(duration, pace=False) -> dict:
    return step_generator(
        duration=duration,
        target='LONG_RUN_PACE',
        description='Long run pace') if pace else step_generator(
        duration=duration,
        target='LONG_RUN_HEART_RATE',
        description='Long run pace')


def marathon_step_generator(target: str, duration, pace=False) -> dict:
    d, s = margin_generator(target)
    return step_generator(
        duration=duration,
        target=d + 'MARATHON_PACE',
        description=s + 'Marathon pace') if pace else step_generator(
        duration=duration,
        target=d + 'MARATHON_HEART_RATE',
        description=s + 'Marathon pace')


def hm_step_generator(target: str, duration, pace=False) -> dict:
    d, s = margin_generator(target)
    return step_generator(
        duration=duration,
        target=d + 'HALF_MARATHON_PACE',
        description=s + 'Half Marathon pace')


def tuneup_step_generator(duration) -> dict:
    return step_generator(duration=duration, target='10KM_PACE', description='10K pace run')


def warmup_step_generator(duration) -> dict:
    return step_generator(type='warmup', duration=duration, target='AEROBIC_HEART_RATE', description='Warm up')


def cooldown_step_generator(duration, pace=False) -> dict:
    return step_generator(
        type='cooldown', duration=duration, target='AEROBIC_PACE', description='Cool down') if pace else step_generator(
        type='cooldown', duration=duration, target='AEROBIC_HEART_RATE', description='Cool down')


def walk_step_generator(duration) -> dict:
    return step_generator(type='rest', duration=duration, target='WALK', description='Walk')


def stride_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator(duration=duration, target='1KM_PACE', description='Strides pace'))
    steps.append(step_generator(type='rest', duration=duration, target='RECOVERY_PACE', description='Recovery pace'))
    return steps


def hill_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator(duration='0:10', target='1KM_PACE', description='Hill climbing'))
    steps.append(step_generator(type='rest', duration='0:20', target='RECOVERY_PACE', description='Recovery pace'))
    return steps


def acceleration_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator(duration='0:30', target='1KM_PACE', description='Accelerations'))
    steps.append(step_generator(type='rest', duration='0:30', target='RECOVERY_PACE', description='Recovery pace'))
    return steps


def series_generator(duration) -> list[dict]:
    steps: list[dict] = []
    match duration:
        case '200m':
            steps.append(step_generator(duration='0.2km', target='1KM_PACE', description='Series @1k pace'))
            steps.append(step_generator(type='rest', duration='0.2km', target='RECOVERY_PACE', description='Recovery'))
        case '300m':
            steps.append(step_generator(duration='0.3km', target='1KM_PACE', description='Series @1k pace'))
            steps.append(step_generator(type='rest', duration='0.3km', target='RECOVERY_PACE', description='Recovery'))
        case '600m':
            steps.append(step_generator(duration='0.6km', target='5KM_PACE', description='Series @5k pace'))
            steps.append(step_generator(type='rest', duration='1:30', target='RECOVERY_PACE', description='Recovery'))
        case '800m':
            steps.append(step_generator(duration='0.8km', target='5KM_PACE', description='Series @5k pace'))
            steps.append(step_generator(type='rest', duration='2:00', target='RECOVERY_PACE', description='Recovery'))
        case '1000m':
            steps.append(step_generator(duration='1km', target='5KM_PACE', description='Series @5k pace'))
            steps.append(step_generator(type='rest', duration='2:30', target='RECOVERY_PACE', description='Recovery'))
        case '1200m':
            steps.append(step_generator(duration='1.2km', target='5KM_PACE', description='Series @5k pace'))
            steps.append(step_generator(type='rest', duration='3:00', target='RECOVERY_PACE', description='Recovery'))
        case '1600m':
            steps.append(step_generator(duration='1.6km', target='5KM_PACE', description='Series @5k pace'))
            steps.append(step_generator(type='rest', duration='4:00', target='RECOVERY_PACE', description='Recovery'))
        case '0:03:00':
            steps.append(step_generator(duration='3:00', target='5KM_PACE', description='Series @5k pace'))
            steps.append(step_generator(type='rest', duration='2:00', target='RECOVERY_PACE', description='Recovery'))
    return steps


def longhill_generator(duration) -> list[dict]:
    steps: list[dict] = []
    type_dur: str = Duration(duration).get_type()
    dur: int | None = Duration.get_value(duration)
    duration_rest: int = 2 * dur if dur is not None else 0
    steps.append(step_generator(duration=duration, target='5KM_PACE', description='Long hill climbing'))
    steps.append(step_generator(type='rest', duration=Duration.get_string(duration_rest, type_dur),
                                target='RECOVERY_PACE', description='Recovery pace'))
    return steps


def anaerobic_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator(duration, '1500M_PACE', description='Series @1500 pace'))
    steps.append(step_generator(type='rest', duration='1:00', target='WALK', description='Recovery pace'))
    return steps


def race_generator(duration, objective):
    match duration:
        case '5km':
            title = '5k race'
            if objective <= 20:
                return race_steps_generator(z4='5km', description=title)
            elif objective <= 25:
                return race_steps_generator(z3='1km', z4='4km', description=title)
            elif objective <= 30:
                return race_steps_generator(z3='2km', z4='3km', description=title)
            else:
                return race_steps_generator(z3='3km', z4='2km', description=title)
        case '6km':
            title = '6k race'
            if objective <= 20:
                return race_steps_generator(z4='6km', description=title)
            elif objective <= 25:
                return race_steps_generator(z3='1km', z4='5km', description=title)
            elif objective <= 30:
                return race_steps_generator(z3='2km', z4='4km', description=title)
            elif objective <= 36:
                return race_steps_generator(z3='3km', z4='3km', description=title)
            else:
                return race_steps_generator(z3='4km', z4='2km', description=title)
        case '10km':
            title = '10k race'
            if objective <= 30:
                return race_steps_generator(z3='4km', z4='6km', description=title)
            elif objective <= 40:
                return race_steps_generator(z3='5km', z4='5km', description=title)
            elif objective <= 50:
                return race_steps_generator(z3='6km', z4='4km', description=title)
            elif objective <= 60:
                return race_steps_generator(z3='7km', z4='3km', description=title)
            else:
                return race_steps_generator(z3='8km', z4='2km', description=title)
        case '15km':
            title = '15k race'
            if objective <= 60:
                return race_steps_generator(z3='10km', z4='5km', description=title)
            elif objective <= 75:
                return race_steps_generator(z3='11km', z4='4km', description=title)
            elif objective <= 90:
                return race_steps_generator(z3='12km', z4='3km', description=title)
            else:
                return race_steps_generator(z3='13km', z4='2km', description=title)
        case '20km':
            title = '20k race'
            if objective <= 70:
                return race_steps_generator(z2='7km', z3='11km', z4='2km', description=title)
            elif objective <= 80:
                return race_steps_generator(z2='8km', z3='10km', z4='2km', description=title)
            elif objective <= 90:
                return race_steps_generator(z2='9km', z3='9km', z4='2km', description=title)
            elif objective <= 100:
                return race_steps_generator(z2='10km', z3='8km', z4='2km', description=title)
            elif objective <= 110:
                return race_steps_generator(z2='11km', z3='7km', z4='2km', description=title)
            elif objective <= 120:
                return race_steps_generator(z2='12km', z3='6km', z4='2km', description=title)
            else:
                return race_steps_generator(z2='13km', z3='5km', z4='2km', description=title)
        case '21.1km':
            title = 'Half marathon race'
            if objective <= 80:
                return race_steps_generator(z2='8km', z3='11km', z4='2.1km', description=title)
            elif objective <= 90:
                return race_steps_generator(z2='9km', z3='10km', z4='2.1km', description=title)
            elif objective <= 100:
                return race_steps_generator(z2='10km', z3='9km', z4='2.1km', description=title)
            elif objective <= 110:
                return race_steps_generator(z2='11km', z3='8km', z4='2.1km', description=title)
            elif objective <= 120:
                return race_steps_generator(z2='12km', z3='7km', z4='2.1km', description=title)
            elif objective <= 130:
                return race_steps_generator(z2='13km', z3='6km', z4='2.1km', description=title)
            else:
                return race_steps_generator(z2='14km', z3='5km', z4='2.1km', description=title)
        case 'marathon':
            title = 'Marathon race'
            if objective <= 150:
                return race_steps_generator(z1='3km', z2='25km', z3='14.2km', description=title)
            elif objective <= 195:
                return race_steps_generator(z1='7km', z2='25km', z3='10.2km', description=title)
            elif objective <= 220:
                return race_steps_generator(z1='10km', z2='25km', z3='7.2km', description=title)
            elif objective <= 240:
                return race_steps_generator(z1='12km', z2='25km', z3='5.2km', description=title)
            else:
                return race_steps_generator(z1='15km', z2='25km', z3='2.2km', description=title)


def step_generator(duration: str,
                   target: str = 'NO_TARGET',
                   type: str = 'interval', description: str = '',
                   category: str | None = None,
                   exerciseName: str | None = None) -> dict:
    return {'type': type, 'duration': duration, 'target': target, 'description': description, 'category': category,
            'exerciseName': exerciseName}


def margin_generator(target: str) -> tuple[str, str]:
    if '>' in target:
        d, target = target.split('>')
        s: str = d + 's quicker than '
        d: str = d + '>'
    elif '<' in target:
        d, target = target.split('<')
        s = d + 's slower than '
        d = d + '<'
    else:
        d = ''
        s = ''
    return d, s


def race_steps_generator(z1=None, z2=None, z3=None, z4=None, description='') -> list[dict]:
    steps: list[dict] = []
    if z1 is not None:
        steps.append(step_generator(duration=z1, target='HEART_RATE_ZONE_1', description=description))
    if z2 is not None:
        steps.append(step_generator(duration=z2, target='HEART_RATE_ZONE_2', description=description))
    if z3 is not None:
        steps.append(step_generator(duration=z3, target='HEART_RATE_ZONE_3', description=description))
    if z4 is not None:
        steps.append(step_generator(duration=z4, target='HEART_RATE_ZONE_4', description=description))
    return steps


def plankpushhold_generator(duration) -> list[dict]:
    steps: list[dict] = []
    med = str(int(int(duration) / 2))
    steps.append(step_generator(
        category='PLANK',
        description='Shoulder taps',
        duration=duration + 'reps',
        exerciseName='STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH'))
    steps.append(step_generator(
        category='PUSH_UP',
        duration=med + 'reps',
        exerciseName='PUSH_UP'))
    steps.append(step_generator(
        category='PLANK',
        description='Shoulder taps',
        duration='lap.button',
        exerciseName='PLANK'))
    steps.append(step_generator(
        type='rest',
        duration='2:00'))
    return steps


def calflunge_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator(
        category='CALF_RAISE',
        duration=duration + 'reps',
        exerciseName='CALF_RAISE'))
    steps.append(step_generator(
        category='LUNGE',
        duration=duration + 'reps',
        exerciseName='LUNGE'))
    steps.append(step_generator(
        category='LUNGE',
        duration=duration + 'reps',
        exerciseName='SIDE_LUNGE'))
    steps.append(step_generator(
        type='rest',
        duration='2:00'))
    return steps


def calfholdlunge_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator(
        category='CALF_RAISE',
        duration=duration + 'reps',
        exerciseName='CALF_RAISE'))
    steps.append(step_generator(
        category='CALF_RAISE',
        description=duration + '-count hold',
        duration='lap.button',
        exerciseName='CALF_RAISE'))
    steps.append(step_generator(
        category='LUNGE',
        duration=duration + 'reps',
        exerciseName='LUNGE'))
    steps.append(step_generator(
        type='rest',
        duration='2:00'))
    return steps


def calfsquathold_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator(
        category='CALF_RAISE',
        duration=duration + 'reps',
        exerciseName='CALF_RAISE'))
    steps.append(step_generator(
        category='SQUAT',
        duration=duration + 'reps',
        exerciseName='SQUAT'))
    steps.append(step_generator(
        category='SQUAT',
        description=duration + '-count hold',
        duration='lap.button',
        exerciseName='SQUAT'))
    steps.append(step_generator(
        type='rest',
        duration='2:00'))
    return steps


def plankpushangel_generator(duration) -> list[dict]:
    steps: list[dict] = []
    med = str(int(int(duration) / 2))
    steps.append(step_generator(
        category='PLANK',
        description='Shoulder taps',
        duration=duration + 'reps',
        exerciseName='STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH'))
    steps.append(step_generator(
        category='PUSH_UP',
        duration=med + 'reps',
        exerciseName='PUSH_UP'))
    steps.append(step_generator(
        category='SHOULDER_STABILITY',
        description='8 reverse angels',
        duration='lap.button',
        exerciseName='LYING_EXTERNAL_ROTATION'))
    steps.append(step_generator(
        type='rest',
        duration='2:00'))
    return steps
