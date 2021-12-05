from math import pi
from random import randrange


def map_to_ascii(image: list, greyscale: dict):
    ascii_art = []

    for row in image:
        ar = []
        for pixel in row:
            ar.append(greyscale[pixel][randrange(len(greyscale[pixel]))])
        ascii_art.append(ar)

    return ascii_art