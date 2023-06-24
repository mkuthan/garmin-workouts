SPORT_TYPES = {
    "running": 1,
    "trail_running": 1,
    "cycling": 2,
    "gravel_cycling": 2,
    "mountain_biking": 2,
    "swimming": 4,
    "strength_training": 5,
    "cardio_training": 6,
    "yoga": 7,
    "pilates": 8,
    "hiit": 9,
    "other": 3
}


INTENSITY_TYPES = {
    "active": 1,
    "rest": 2,
    "warmup": 3,
    "cooldown": 4,
}

STEP_TYPES = {
    "warmup": 1,
    "cooldown": 2,
    "run": 3,
    "interval": 3,
    "recovery": 4,
    "rest": 5,
    "repeat": 6,
    "other": 7
}

END_CONDITIONS = {
    "lap.button": 1,
    "time": 2,
    "distance": 3,
    "calories": 4,
    "iterations": 7,
    "fixed.rest": 8,
    "fixed.repetition": 9,
    "training.peaks.tss": 11,
    "repetition.time": 12,
    "time.at.valid.cda": 13,
    "power.last.lap": 14,
    "max.power.last.lap": 15,
    "reps": 10,
    "power": 5,         # Potencia por encima de un umbral ("endConditionCompare": "gt")
                        # Potencia por debajo de un umbral ("endConditionCompare": "lt")
    "heart.rate": 6,    # Pulsaciones por encima de un umbral ("endConditionCompare": "lt")
                        # Pulsaciones por debajo de un umbral ("endConditionCompare": "gt")
}

STROKE_TYPES = {
    "any_stroke": 1,         # Cualquiera
    "backstroke": 2,         # Espalda
    "breaststroke": 3,       # Braza
    "drill": 4,              # Tecnica
    "fly": 5,                # Mariposa
    "free": 6,               # Croll
    "individual_medley": 7,  # Estilos
    "mixed": 8,
}

EQUIPMENT_TYPES = {
    "fins": 1,          # Aletas
    "kickboard": 2,     # Tabla
    "paddles": 3,       # Palas
    "pull_buoy": 4,     # Pull buoy
    "snorkel": 5,       # Tubo buceo
    "none": 0           # Sin equipo
}

POOL_LENGTHS = {
    "short": 25,
    "olympic": 50
}

TARGET_TYPES = {
    "no.target": 1,
    "power.zone": 2,
    "cadence.zone": 3,
    "cadence": 3,
    "heart.rate.zone": 4,
    "speed.zone": 5,
    "pace.zone": 6,  # meters per second
    "grade": 7,
    "heart.rate.lap": 8,
    "power.lap": 9,
    "power.3s": 10,
    "power.10s": 11,
    "power.30s": 12,
    "speed.lap": 13,
    "swim.stroke": 14,
    "resistance": 15,
    "power.curve": 16
}
