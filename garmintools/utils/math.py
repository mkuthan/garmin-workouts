import numpy as np


def moving_average(x, n):
    return np.convolve(x, np.ones((n,)) / n, mode="valid")


def normalized_power(x):
    return np.sqrt(np.sqrt(np.mean(moving_average(x, 30) ** 4)))


def intensity_factor(norm_pwr, ftp):
    return norm_pwr / ftp


def training_stress_score(seconds, norm_pwr, ftp):
    int_fct = intensity_factor(norm_pwr, ftp)
    return (seconds * norm_pwr * int_fct) / (ftp * 3600) * 100
