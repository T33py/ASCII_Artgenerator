def print_image_representation(image: list):
    rep = ""
    for row in image:
        for pixel in row:
            rep = rep + pixel
        rep = rep + "\n"
    return rep

def print_to_file(file: str, image: list):
    f = open(file, "w")
    f.write("")
    f.close()
    f = open(file, "a")
    for row in image:
        for pixel in row:
            f.write(str(pixel))
        f.write("\n")


def write_ranking(file: str, letters: list):
    f = open(file, "w")
    f.write("")
    f.close()
    f = open(file, "a")
    for letter in letters:
        f.write(f'{letter}\n')
