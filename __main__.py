import os
import sys
import logging
from utility.arg_reader import read_args
from image_representation_printer import print_to_file
from greyscale_image import convert_to_greyscale
from utility.font_profiler import read_letter_ranking
from ascii_mapper import map_to_ascii

def main():
    # read args
    f_in = ''
    f_out = ''
    try:
        (uf_in, uf_out) = read_args(sys.argv)
        
        if uf_in != "":
            f_in = uf_in

        if uf_out != "":
            f_out = uf_out
            
    except ValueError as e:
        logging.error(f"Invalid argument assignment: {e}")
        return 1
    except Exception as e:
        logging.error(f"failed to read arguments: {e}")
        return 2


    # setup
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f'assets\\letters.ranked')
    greyscale_to_char = read_letter_ranking(filename)
    
    # user input
    if f_in == "":
        raise ValueError("No image specified. Use -i to specify an image to convert")
    filename = os.path.join(dirname, f'assets\\{f_in}')

    if not os.path.isfile(filename):
        logging.error(f'Image: {filename} not found')
        return 3
    
    print(f"converting {filename} to greyscale")
    greyscaled_image = convert_to_greyscale(filename)
    
    # computation
    print("Converting to ascii")
    ascii_art = map_to_ascii(greyscaled_image, greyscale_to_char)

    # user output
    if f_out == "":
        f_out = 'default.txt'
        print(f'No output file specified - printing to {f_out}')
    
    outdir = os.path.join(dirname, 'out')
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    filename = os.path.join(outdir, f'{f_out}')
    print(f'printing image to {filename}')
    print_to_file(filename, ascii_art)
    
    print("done")
    return 0

if __name__ == "__main__":
    main()
