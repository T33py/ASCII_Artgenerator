import os
from image_representation_printer import print_image_representation, print_to_file
from greyscale_image import convert_to_greyscale
from utility.font_profiler import generate_weightings, map_to_greyscale, read_profile, read_letter_ranking
from ascii_mapper import map_to_ascii

def main():
    print("starting")
    
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    # ws = generate_weightings(letters)
    # greyscale_to_char = map_to_greyscale(letters, ws)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'assets\\letters.ranked')
    greyscale_to_char = read_letter_ranking(filename)
    filename = os.path.join(dirname, 'assets\\calibration3.jpg')
    greyscaled_image = convert_to_greyscale(filename)
    ascii_art = map_to_ascii(greyscaled_image, greyscale_to_char)
    # print_image_representation(greyscaled_image)
    print("printing image to tst out")
    filename = os.path.join(dirname, 'out\\tst.txt')
    print_to_file(filename, ascii_art)
    
    print("done")
    return 0

if __name__ == "__main__":
    main()
