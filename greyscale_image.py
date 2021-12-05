from PIL import Image

tst = "C:/Users/Thorb/source/repos/ASCIIArtGeneratorV3/assets/rgb_tst.jpg"

# Create an array containing the greyscale value of the image pixels
def convert_to_greyscale(img: str):
    print(f"converting {img} to greyscale")
    gs_img = []
    im = Image.open(img)
    print(im.size)
    width = im.size[0]
    height = im.size[1]

    for y in range(height):
        row = []

        for x in range(width):
            pixel = im.getpixel((x, y))
            row.append((pixel[0] + pixel[1] + pixel[2]) // 3)

        gs_img.append(row)


    return gs_img


# convert_to_greyscale(tst)