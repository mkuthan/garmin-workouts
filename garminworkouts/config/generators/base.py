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
