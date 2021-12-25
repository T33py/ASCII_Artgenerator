from math import pi
from random import randrange

# map the given greyscale to the individual pixels of the image
def map_to_ascii(image: list, greyscale: dict):
    ascii_art = []

    for row in image:
        ar = []
        for pixel in row:
            ar.append(greyscale[pixel][randrange(len(greyscale[pixel]))])
        ascii_art.append(ar)

    return ascii_art