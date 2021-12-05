def print_image_representation(image: list):
    for row in image:
        print(f"{str(row)}\n")

def print_to_file(file: str, image: list):
    f = open(file, "w")
    f.write("")
    f.close()
    f = open(file, "a")
    for row in image:
        for pixel in row:
            f.write(str(pixel))
        f.write("\n")