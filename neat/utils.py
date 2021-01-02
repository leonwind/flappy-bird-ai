import random


def rand_uni_val() -> float:
    """Return a random float on the interval [0, 1]"""
    return random.uniform(0, 1)


def rand_bool() -> bool:
    """Return a random bool"""
    # use random() < 0.5 instead of choice([True, False]) since choice
    # is substantially slower
    return rand_uni_val() < 0.5


def pos_or_neg() -> int:
    """Return either -1 or 1"""
    # use random() < 0.5 instead of choice([True, False]) since choice
    # is substantially slower
    return -1 if rand_uni_val() < 0.5 else 1
