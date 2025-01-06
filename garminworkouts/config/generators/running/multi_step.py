from garminworkouts.config.generators.base import step_generator
from garminworkouts.models.duration import Duration


def Rseries_generator(duration, objective) -> list[dict]:
    steps: list[dict] = []
    for i in range(2):
        step_type = 'interval' if i == 0 else 'rest'
        if int(objective[0][1]) <= int(objective[1][1]):
            step_type = 'rest' if i == 0 else 'interval'
        steps.append(step_generator(
            type=step_type,
            duration=duration[i],
            target=objective[i],
            description=f'{objective[i]} pace'))
    return steps


def stride_generator(duration) -> list[dict]:
    return [
        step_generator(duration=duration, target='1KM_PACE', description='Strides pace'),
        step_generator(type='rest', duration=duration, target='RECOVERY_PACE', description='Recovery pace')
    ]


def hill_generator(duration) -> list[dict]:
    return [
        step_generator(duration='0:10', target='1KM_PACE', description='Hill climbing'),
        step_generator(type='rest', duration='0:20', target='RECOVERY_PACE', description='Recovery pace')
    ]


def acceleration_generator(duration) -> list[dict]:
    return [
        step_generator(duration='0:30', target='1KM_PACE', description='Accelerations'),
        step_generator(type='rest', duration='0:30', target='RECOVERY_PACE', description='Recovery pace')
    ]


def series_generator(duration) -> list[dict]:
    steps: list[dict] = []
    duration_map = {
        '200m': ('0.2km', '1KM_PACE', '1k', '0.2km'),
        '300m': ('0.3km', '1KM_PACE', '1k', '0.3km'),
        '600m': ('0.6km', '5KM_PACE', '5k', '1:30'),
        '800m': ('0.8km', '5KM_PACE', '5k', '2:00'),
        '1000m': ('1km', '5KM_PACE', '5k', '2:30'),
        '1200m': ('1.2km', '5KM_PACE', '5k', '3:00'),
        '1600m': ('1.6km', '5KM_PACE', '5k', '4:00'),
        '0:03:00': ('3:00', '5KM_PACE', '5k', '2:00')
    }
    if duration in duration_map:
        series_dur, target_dur, label, rest_dur = duration_map[duration]
        steps.append(step_generator(duration=series_dur, target=target_dur, description=f'Series @{label} pace'))
        steps.append(step_generator(type='rest', duration=rest_dur, target='RECOVERY_PACE', description='Recovery'))
    return steps


def longhill_generator(duration) -> list[dict]:
    dur = Duration.get_value(duration)
    duration_rest = 2 * dur if dur is not None else 0
    return [
        step_generator(duration=duration, target='5KM_PACE', description='Long hill climbing'),
        step_generator(type='rest', duration=Duration.get_string(duration_rest, Duration(duration).get_type()),
                       target='RECOVERY_PACE', description='Recovery pace')
    ]


def anaerobic_generator(duration) -> list[dict]:
    return [
        step_generator(duration=duration, target='1500M_PACE', description='Series @1500 pace'),
        step_generator(type='rest', duration='1:00', target='RECOVERY_PACE', description='Recovery pace')
    ]


def race_generator(duration, objective):
    title_map = {
        '5km': '5k race',
        '6km': '6k race',
        '10km': '10k race',
        '15km': '15k race',
        '20km': '20k race',
        '21.1km': 'Half marathon race',
        'marathon': 'Marathon race'
    }
    steps_map = {
        '5km': [
            (20, 'z4', '5km'),
            (25, 'z3', '1km', 'z4', '4km'),
            (30, 'z3', '2km', 'z4', '3km'),
            (float('inf'), 'z3', '3km', 'z4', '2km')
            ],
        '6km': [
            (20, 'z4', '6km'),
            (25, 'z3', '1km', 'z4', '5km'),
            (30, 'z3', '2km', 'z4', '4km'),
            (36, 'z3', '3km', 'z4', '3km'),
            (float('inf'), 'z3', '4km', 'z4', '2km')
            ],
        '10km': [
            (30, 'z3', '4km', 'z4', '6km'),
            (40, 'z3', '5km', 'z4', '5km'),
            (50, 'z3', '6km', 'z4', '4km'),
            (60, 'z3', '7km', 'z4', '3km'),
            (float('inf'), 'z3', '8km', 'z4', '2km')
            ],
        '15km': [
            (60, 'z3', '10km', 'z4', '5km'),
            (75, 'z3', '11km', 'z4', '4km'),
            (90, 'z3', '12km', 'z4', '3km'),
            (float('inf'), 'z3', '13km', 'z4', '2km')
            ],
        '20km': [
            (70, 'z2', '7km', 'z3', '11km', 'z4', '2km'),
            (80, 'z2', '8km', 'z3', '10km', 'z4', '2km'),
            (90, 'z2', '9km', 'z3', '9km', 'z4', '2km'),
            (100, 'z2', '10km', 'z3', '8km', 'z4', '2km'),
            (110, 'z2', '11km', 'z3', '7km', 'z4', '2km'),
            (120, 'z2', '12km', 'z3', '6km', 'z4', '2km'),
            (float('inf'), 'z2', '13km', 'z3', '5km', 'z4', '2km')
            ],
        '21.1km': [
            (80, 'z2', '8km', 'z3', '11km', 'z4', '2.1km'),
            (90, 'z2', '9km', 'z3', '10km', 'z4', '2.1km'),
            (100, 'z2', '10km', 'z3', '9km', 'z4', '2.1km'),
            (110, 'z2', '11km', 'z3', '8km', 'z4', '2.1km'),
            (120, 'z2', '12km', 'z3', '7km', 'z4', '2.1km'),
            (130, 'z2', '13km', 'z3', '6km', 'z4', '2.1km'),
            (float('inf'), 'z2', '14km', 'z3', '5km', 'z4', '2.1km')
            ],
        'marathon': [
            (150, 'z1', '3km', 'z2', '25km', 'z3', '14.2km'),
            (195, 'z1', '7km', 'z2', '25km', 'z3', '10.2km'),
            (220, 'z1', '10km', 'z2', '25km', 'z3', '7.2km'),
            (240, 'z1', '12km', 'z2', '25km', 'z3', '5.2km'),
            (float('inf'), 'z1', '15km', 'z2', '25km', 'z3', '2.2km')
            ]
    }
    title = title_map.get(duration, 'Race')
    for limit, *zones in steps_map.get(duration, []):
        if objective <= limit:
            return race_steps_generator(**{zones[i]: zones[i+1] for i in range(0, len(zones), 2)}, description=title)
    return []


def race_steps_generator(z1=None, z2=None, z3=None, z4=None, description='') -> list[dict]:
    steps: list[dict] = []
    zones = [z1, z2, z3, z4]
    targets = ['HEART_RATE_ZONE_1', 'HEART_RATE_ZONE_2', 'HEART_RATE_ZONE_3', 'HEART_RATE_ZONE_4']
    for zone, target in zip(zones, targets):
        if zone is not None:
            steps.append(step_generator(duration=zone, target=target, description=description))
    return steps
