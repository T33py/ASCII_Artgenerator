from PIL import Image

tst = "C:/Users/Thorb/source/repos/ASCIIArtGeneratorV3/assets/rgb_tst.jpg"

# Create a 2 dimensional array containing the greyscale value of the image pixels
def convert_to_greyscale(img: str):
    im = Image.open(img)
    # print(im.size)

    return greyscale(im)

# Create a 2 dimensional array containing the greyscale value of the image pixels with the image scaled to the requested size
def scaled_convert_to_greyscale(img: str, width: int, height: int):
    im = Image.open(img)
    if width is None:
        width = im.size[0]
    if height is None:
        height = im.size[1]
        
    r_im = im.resize((width, height))
    return greyscale(r_im)


# Convert the given image to greyscale
def greyscale(im: Image):
    gs_img = []
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