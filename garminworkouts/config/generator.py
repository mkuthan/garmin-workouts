from garminworkouts.models.duration import Duration


def recovery_step_generator(duration, pace=False) -> dict:
    return step_generator('recovery', duration, 'RECOVERY_PACE', 'Recovery pace') if pace else step_generator(
        'recovery', duration, 'RECOVERY_HEART_RATE', 'Recovery pace')


def aerobic_step_generator(duration, pace=False) -> dict:
    return step_generator('interval', duration, 'AEROBIC_PACE', 'Aerobic pace') if pace else step_generator(
        'interval', duration, 'AEROBIC_HEART_RATE', 'Aerobic pace')


def lt_step_generator(target: str, duration, pace=False) -> dict:
    d, s = margin_generator(target)
    return step_generator('interval', duration, d + 'THRESHOLD_PACE', s + 'Threshold pace') if pace else step_generator(
        'interval', duration, d + 'THRESHOLD_HEART_RATE', s + 'Threshold pace')


def lr_step_generator(duration, pace=False) -> dict:
    return step_generator('interval', duration, 'LONG_RUN_PACE', 'Long run pace') if pace else step_generator(
        'interval', duration, 'LONG_RUN_HEART_RATE', 'Long run pace')


def marathon_step_generator(target: str, duration, pace=False) -> dict:
    d, s = margin_generator(target)
    return step_generator('interval', duration, d + 'MARATHON_PACE', s + 'Marathon pace') if pace else step_generator(
        'interval', duration, d + 'MARATHON_HEART_RATE', s + 'Marathon pace')


def hm_step_generator(target: str, duration, pace=False) -> dict:
    d, s = margin_generator(target)
    return step_generator('interval', duration, d + 'HALF_MARATHON_PACE', s + 'Half Marathon pace')


def tuneup_step_generator(duration) -> dict:
    return step_generator('interval', duration, '10KM_PACE', '10K pace run')


def warmup_step_generator(duration) -> dict:
    return step_generator('warmup', duration, 'AEROBIC_HEART_RATE', 'Warm up')


def cooldown_step_generator(duration, pace=False) -> dict:
    return step_generator('cooldown', duration, 'AEROBIC_PACE', 'Cool down') if pace else step_generator(
        'cooldown', duration, 'AEROBIC_HEART_RATE', 'Cool down')


def walk_step_generator(duration) -> dict:
    return step_generator('rest', duration, 'WALK', 'Walk')


def stride_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator('interval', duration, '1KM_PACE', 'Strides pace'))
    steps.append(step_generator('rest', duration, 'RECOVERY_PACE', 'Recovery pace'))
    return steps


def hill_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator('interval', '0:10', '1KM_PACE', 'Hill climbing'))
    steps.append(step_generator('rest', '0:20', 'RECOVERY_PACE', 'Recovery pace'))
    return steps


def acceleration_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator('interval', '0:30', '1KM_PACE', 'Accelerations'))
    steps.append(step_generator('rest', '0:30', 'RECOVERY_PACE', 'Recovery pace'))
    return steps


def series_generator(duration) -> list[dict]:
    steps: list[dict] = []
    match duration:
        case '200m':
            steps.append(step_generator('interval', '0.2km', '1KM_PACE', 'Series @1k pace'))
            steps.append(step_generator('rest', '0.2km', 'RECOVERY_PACE', 'Recovery'))
        case '300m':
            steps.append(step_generator('interval', '0.3km', '1KM_PACE', 'Series @1k pace'))
            steps.append(step_generator('rest', '0.3km', 'RECOVERY_PACE', 'Recovery'))
        case '600m':
            steps.append(step_generator('interval', '0.6km', '5KM_PACE', 'Series @5k pace'))
            steps.append(step_generator('rest', '1:30', 'RECOVERY_PACE', 'Recovery'))
        case '800m':
            steps.append(step_generator('interval', '0.8km', '5KM_PACE', 'Series @5k pace'))
            steps.append(step_generator('rest', '2:00', 'RECOVERY_PACE', 'Recovery'))
        case '1000m':
            steps.append(step_generator('interval', '1km', '5KM_PACE', 'Series @5k pace'))
            steps.append(step_generator('rest', '2:30', 'RECOVERY_PACE', 'Recovery'))
        case '1200m':
            steps.append(step_generator('interval', '1.2km', '5KM_PACE', 'Series @5k pace'))
            steps.append(step_generator('rest', '3:00', 'RECOVERY_PACE', 'Recovery'))
        case '1600m':
            steps.append(step_generator('interval', '1.6km', '5KM_PACE', 'Series @5k pace'))
            steps.append(step_generator('rest', '4:00', 'RECOVERY_PACE', 'Recovery'))
        case '0:03:00':
            steps.append(step_generator('interval', '3:00', '5KM_PACE', 'Series @5k pace'))
            steps.append(step_generator('rest', '1:30', 'RECOVERY_PACE', 'Recovery'))
    return steps


def longhill_generator(duration) -> list[dict]:
    steps: list[dict] = []
    type_dur: str = Duration(duration).get_type()
    dur: int | None = Duration.get_value(duration)
    duration_rest: int = 2 * dur if dur is not None else 0
    steps.append(step_generator('interval', duration, '5KM_PACE', 'Long hill climbing'))
    steps.append(step_generator('rest', Duration.get_string(duration_rest, type_dur), 'RECOVERY_PACE', 'Recovery pace'))
    return steps


def anaerobic_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(step_generator('interval', duration, '1500M_PACE', 'Series @1500 pace'))
    steps.append(step_generator('rest', '1:00', 'WALK', 'Recovery pace'))
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


def step_generator(type: str, duration: str, target: str, description: str) -> dict:
    return {'type': type, 'duration': duration, 'target': target, 'description': description}


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
        steps.append(step_generator('interval', z1, 'HEART_RATE_ZONE_1', description))
    if z2 is not None:
        steps.append(step_generator('interval', z2, 'HEART_RATE_ZONE_2', description))
    if z3 is not None:
        steps.append(step_generator('interval', z3, 'HEART_RATE_ZONE_3', description))
    if z4 is not None:
        steps.append(step_generator('interval', z4, 'HEART_RATE_ZONE_4', description))
    return steps
