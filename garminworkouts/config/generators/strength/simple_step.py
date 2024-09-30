from garminworkouts.config.generators.base import step_generator
from garminworkouts.models.strength_map import MAP


def exercise_generator(category='', exercise_name='', duration='', execution='') -> dict:
    if category not in MAP:
        raise KeyError(f"Category {category} not found in strength exercises.")
    else:
        fields = MAP[category]

    if exercise_name not in fields:
        raise ValueError(f"Exercise {exercise_name} not found in {category}.")

    description: str = exercise_name.replace('_', ' ').title()

    if execution == 'reps':
        return step_generator(
            category=category,
            description=description,
            duration=f"{duration}reps",
            exerciseName=exercise_name)
    elif execution == 'hold':
        return step_generator(
            category=category,
            description=f"{duration}-count hold",
            duration='lap.button',
            exerciseName=exercise_name)
    else:
        return step_generator(
            category=category,
            description=f"Max {description}s",
            duration='lap.button',
            exerciseName=exercise_name)


def rest_generator(duration) -> dict:
    return step_generator(
        type='rest',
        duration=duration)
