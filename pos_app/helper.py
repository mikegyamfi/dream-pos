import random


def ref_generator(shop_name):
    number = random.randint(11111, 99999)
    letter = shop_name[0].upper()
    return f"{letter}{number}"

