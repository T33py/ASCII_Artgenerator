from random import randint
from image_representation_printer import print_to_file
import os
import ast
from greyscale_image import convert_to_greyscale

dev_test_folder = "C:\\Users\\Thorb\\source\\repos\\ASCIIArtGeneratorV3\\"
color_gradiant = 256

# uses images of the letters in the font marked as the character contained to generate weights of letters for the ascii art generation
# checks for <letter>.png in the assets folder where letter is each of the letters in the provided list.
# files containing lowercase letters are marked by an underscore behind the letter <letter>_.png (windows filesystem is case insensitive)
def generate_weightings(letters: list):
    weightings = { " ": 255 }
    for letter in letters:
        filename = f'{dev_test_folder}\\assets\\{letter}.png'
        if letter.islower():
            f'{dev_test_folder}\\assets\\{letter}_.png'
        if os.path.exists(filename):
            gw = calculate_colour_weight(filename)
            # even if lowercase letters use the same ammount of black pixels they are generally percieved as less dense
            if letter.islower():
                gw -= 25
            weightings[letter] = gw
        else:
            weightings[letter] = -1
    


    letters.append(' ')
    return weightings

# calculate the average greyscale value of this letter
def calculate_colour_weight(image: str):
    img_gr = convert_to_greyscale(image)
    greyscale_weight = 0
    pixelcount = 0
    for row in img_gr:
        for pixel_value in row:
            greyscale_weight += pixel_value
        
        pixelcount += len(row)
    greyscale_weight = greyscale_weight // pixelcount
    return greyscale_weight

# Takes a list of letters and a dictionary containing a greyscale mapping for each.
# The letters are mapped into a dicitonary containing a list of letters indexed by the greyscale value.
def map_to_greyscale(letters: list, values: dict):
    scale_mapping = {}
    letterclasses = {}

    # generate a dictionary of distinct letter greyscale values
    for letter in letters:
        if values[letter] != -1:
            if values[letter] in letterclasses:
                letterclasses[values[letter]].append(letter)
            else:
                letterclasses[values[letter]] = [letter]
    
    print(str(letterclasses))

    # map letterclasses to the greyscale
    # the greyscale is comprised of 256 values
    keys = []
    for key in letterclasses.keys():
        keys.append(key)

    interval = color_gradiant // len(letterclasses)
    choose_class = []
    idx = 0
    count = 0
    for val in range(color_gradiant):
        choose_class.append(keys[idx])
        count += 1
        if count > interval:
            count = 0
            if idx + 1 < len(keys):
                idx += 1
    
    for idx in range(color_gradiant):
        scale_mapping[idx] = letterclasses[choose_class[idx]]

    return scale_mapping

# Takes a file containing all the letters to use for the art sepparated by '\n'.
# The letters should be ordered by their greyscale value from darkest to lightest..
# The letters are mapped into a dicitonary containing a list of letters indexed by the greyscale value.
def read_letter_ranking(file: str):
    formatted_ranking = read_letters(file)
    return create_greyscale_mapping(formatted_ranking)

def read_letters(file: str):
    with open(file) as f:
        content = f.read()
        ranking = content.split('\n')
        formatted_ranking = []
        for letter in ranking:
            letter.strip()
            if letter != "":
                formatted_ranking.append(letter[0])
        formatted_ranking.append(' ')
    return formatted_ranking

def create_greyscale_mapping(letters: list):
    scale_mapping = {}
    interval = color_gradiant // len(letters)
    remainder = color_gradiant % interval # we will need to pad up to len(formatted_ranking) -1 letters to fill out the gradient - we keep track of it with this variable
    remainder_used = False
    choose_class = []
    letter_index = 0
    count = 0
    for val in range(color_gradiant):
        choose_class.append(letters[letter_index])
        count += 1
        # when we have the correct part of the gradient matched to this letter -> got to the next letter if we have one (pad whitespace untill we are done)
        if count >= interval:
            # place letters denser in the darker tones, this will probably be less noticeable
            # last remainder will allways be given as whitespace since 256/1 == 256 which is not in range(256)
            if remainder > 0 and color_gradiant / remainder < len(choose_class) and not remainder_used:
                remainder -= 1
                remainder_used = True
            elif letter_index + 1 < len(letters):
                count = 0
                letter_index += 1
                remainder_used = False
    
    for letter_index in range(color_gradiant):
        scale_mapping[letter_index] = choose_class[letter_index]

    return scale_mapping
    


# for running funciton tests
def tst():
    print(f"default folder: {dev_test_folder}")
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    filename = os.path.join(dev_test_folder, 'assets\\letters.ranked')
    print("generating weights")
    gs = read_letter_ranking(filename)
    
    letters_ranked = ""
    for key in gs:
        for letter in gs[key]:
            if not letter in letters_ranked:
                letters_ranked = letters_ranked + letter

    print(letters_ranked)
        


# tst()