def recovery_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'RECOVERY_PACE'
    step['description'] = 'Recovery pace'

    return step


def aerobic_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'AEROBIC_PACE'
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
    step['target'] = 'LONG_RUN_PACE'
    step['description'] = 'Long run pace'

    return step


def marathon_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'MARATHON_PACE'
    step['description'] = 'Marathon pace run'

    return step


def hm_step_generator(duration):
    step = {}
    step['type'] = 'run'
    step['duration'] = duration
    step['target'] = 'HALF_MARATHON_PACE'
    step['description'] = 'Half Marathon pace'

    return step


def cooldown_step_generator(duration):
    step = {}
    step['type'] = 'cooldown'
    step['duration'] = duration
    step['target'] = 'AEROBIC_PACE'
    step['description'] = 'Aerobic pace'

    return step
