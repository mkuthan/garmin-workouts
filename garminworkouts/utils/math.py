import numpy as np


def moving_average(x, n) -> float:
    return np.convolve(x, np.ones((n,)) / n, mode="valid")


def normalized_power(x) -> float:
    return np.sqrt(np.sqrt(np.mean(moving_average(x, 30) ** 4)))


def intensity_factor(norm_pwr: float, ftp: float) -> float:
    return norm_pwr / ftp


def training_stress_score(seconds: float, norm_pwr: float, ftp: float) -> float:
    int_fct = intensity_factor(norm_pwr, ftp)
    return (seconds * norm_pwr * int_fct) / (ftp * 3600) * 100
