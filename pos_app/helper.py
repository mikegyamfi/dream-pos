import random


def ref_generator(prefix):
    number = random.randint(11111, 99999)
    prefix = prefix
    return f"{prefix}{number}"

