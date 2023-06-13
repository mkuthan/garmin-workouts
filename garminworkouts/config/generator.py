def recovery_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'RECOVERY_HEART_RATE'
    step['description'] = 'Recovery pace'

    return step


def aerobic_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'AEROBIC_HEART_RATE'
    step['description'] = 'Aerobic pace'

    return step


def lt_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'HALF_MARATHON_PACE'
    step['description'] = 'Threshold pace'

    return step


def lr_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'LONG_RUN_HEART_RATE'
    step['description'] = 'Long run pace'

    return step


def marathon_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'MARATHON_HEART_RATE'
    step['description'] = 'Marathon pace run'

    return step


def hm_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'HALF_MARATHON_PACE'
    step['description'] = 'Half Marathon pace'

    return step


def tuneup_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = '10KM_PACE'
    step['description'] = '10K pace run'

    return step


def cooldown_step_generator(duration):
    step = {}
    step['type'] = 'cooldown'
    step['duration'] = duration
    step['target'] = 'AEROBIC_HEART_RATE'
    step['description'] = 'Aerobic pace'

    return step
