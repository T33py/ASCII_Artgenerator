[WIP] Generate ascii art for an image based on the "currier new" font.
The reason why currier new is the font of choise is that it is both singlespaced (easier to program) and the default font for Notepad++ which is a great tool for viewing your generated art in its full splendour.

This program uses PIL to retrieve image information

Images should be in JPG format (.jpg or .jpeg extension). Other formats will probably be added later.

Example of use: Place the __house.jpg__ file in the assets folder and execute `.\ASCIIArtGeneratorV3\ -i house.jpg -o house.txt`

Letters are mapped to the greyscale in accordance with the letters.ranked file found in the assets folder. They are ordered darkest to lightest. To add your own letters just insert them into that file at the appropriate line. The letters are sepperated by the newline symbol and only the first letter of each line is included to avoid including random whitespaces in the art. 

Input images specified with the "-i \<name\>.\<extension\>" argument will be read from the assets folder.

Output text files specified with the "-o \<name\>.\<extension\>" will be placed in the out folder.

The font_profiler.py file contains functions from my iteration of creaing a system for ranking letters according to the percieved greyscale value when zoomed out. 
- generate_weightings: This function is used to approximate the greyscale value of a letter based on a sample image. My samples are found in the assets folder.
- map_to_greyscale: This function maps the letters profiled to a greyscale dictionary. I used a print of this for the initial version of the letters.ranked file which is used to generate the actual greyscale used in the images.
- read_letter_ranking: This function reads a file containing letters ordered according to their percieved greyscale tone and sepperated by newline characters. The letters contained will be mapped to each of the values in the greyscale gradient.

TODO:
 - Parametize better
 - Comment better
 - ??
 - Profit
