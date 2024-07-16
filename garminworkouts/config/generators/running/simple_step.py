from garminworkouts.config.generators.base import margin_generator, step_generator


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
