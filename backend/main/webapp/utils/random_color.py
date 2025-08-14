import random


def random_color():
    return f'rgb({random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)})'
