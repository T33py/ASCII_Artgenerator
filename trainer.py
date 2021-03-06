import os
import threading
import time
from random import randint, triangular
from typing import Literal
from PIL import Image, ImageFont, ImageDraw
from greyscale_image import greyscale, scaled_convert_to_greyscale
from image_representation_printer import print_image_representation, print_to_file, write_ranking
from ascii_mapper import map_to_ascii
from utility.font_profiler import create_greyscale_mapping, read_letters
from trainee import LetterPicker


dev_folder = "C:\\Users\\Thorb\\source\\repos\\ASCIIArtGeneratorV3"
font_size = 10
if '__file__' in globals():
    folder = __file__
else:
    folder = dev_folder
training_folder = os.path.join(folder, "training")
if not os.path.isdir(training_folder):
    os.mkdir(training_folder)


# runs the training function and reports results to the runner
class Optimizer (threading.Thread):
    def __init__(self, threadID:int, letter:str, dashboard:dict, finished:dict, report_back:dict):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = letter
        self.dashboard = dashboard
        self.report_back = report_back
        self.finished = finished
    def run(self):
        print(f'starting thread: {str(self.threadID)}')
        self.dashboard[self.threadID] = True
        try:
            raise "todo"
            result = train()
            self.report_back[result[2]] = (result[1], self.name)
        finally:
            self.finished[self.threadID] = True
            self.dashboard[self.threadID] = False
        print(f'thread {self.threadID} done')
        return

# run optimizers and keep track of progress made
def runner(letters: list, gs_image: list, generation: int):
    # threads currently running
    dashboard = {}
    # jobs to complete
    job_started = {}
    job_done = {}
    # reports of the best performing permutation of each job
    best_performers = {}
    
    threads_started = 0
    mutation_dist = 1
    threads_running = []
        
    def get_running_threads():
        running = []
        for t in dashboard:
            if dashboard[t]:
                running.append(t)
        return running

    def check_done():
        done = True
        for t in job_done:
            done = job_done[t] and done
        
        return done
    
    def get_next_job():
        for t in job_started:
            if not job_started[t]:
                return t
        return None

    def report_best():
        if len(best_performers.keys()) > 0:
            best_diff = 99999999999999999999999999999999999999999 # todo figure out how to do int.maxval
            for diff in best_performers:
                if diff < best_diff:
                    best_diff = diff

            best = best_performers[best_diff][0]
            print(f'best found in {best_performers[best_diff][1]} with a score of {str(best_diff)}')
            if best_performers[best_diff][1] != 'baseline':
                write_ranking(os.path.join(training_folder, 'best_found.ranked'), best)
                ascii = render_ascii(letters, gs_image, 'current_best', True, True)
                print_to_file(os.path.join(training_folder, 'current_best.txt'), ascii)
            

    # setup dashboard and todolist
    for tid in range(len(letters)):
        dashboard[tid] = False
        job_started[tid] = False
        job_done[tid] = False

    # create a reference for the initial setup
    rendered_ascii = render_ascii(letters, gs_image, 'baseline', True, True)
    print_to_file(os.path.join(training_folder, 'baseline.txt'), create_ascii_art(letters, gs_image))
    baseline = calculate_diff(rendered_ascii, gs_image)
    best_performers[baseline] = (letters, 'baseline')

    while not check_done():
        current_ts = get_running_threads()
        if current_ts != threads_running:
            report_best()
            threads_running = get_running_threads() 
            print(f'{str(threads_running)} threads running')

        if len(threads_running) < 8:
            next_job = get_next_job()
            if next_job is not None and next_job < len(letters) - mutation_dist:
                threads_started += 1
                work = mutate(letters.copy(), next_job)
                job_started[next_job] = True
                opt = Optimizer(next_job, f'g{str(generation)}t{next_job}', work, gs_image, 3, dashboard, best_performers)
                opt.start()
        time.sleep(2)

    
    report_best()
    return "DONE"
    
# Search the given space for better permutations
def train(trainee: LetterEvaluator, iterations: int):
    for iter in range(iterations):
        pixels = []
        for x in range(9):
            gsv = randint(0, 255)
            pixels.append(gsv)
        trainee.train(pixels)

    return trainee

# mutate the list of letters by swapping 2 letters at swap and swap+1
def mutate(letters: list, swap: int, dist = 1):
    pivot = swap
    d_up = pivot
    d_down = len(letters) - pivot
    for val in range(dist):
        if len(letters) < pivot + 1:
            letter1 = letters[pivot]
            letter2 = letters[pivot + 1]
            letters[pivot] = letter2
            letters[pivot + 1] = letter1
            pivot += 1

    return letters

# calculate the total dieviation between 2 greyscale images based on a pixel by pixel differential
def calculate_diff(ascii_img: list, gs_image: list):
    diff = 0
    for x in range(len(ascii_img)):
        for y in range(len(ascii_img[x])):
            diff += abs(ascii_img[x][y] - gs_image[x][y])

    return diff

# create a render of the ascii created -> scale it to the correct image size -> return it as a greyscale image
def render_ascii(letters: list, gs_image: list, render_name='', render_upscaled=False, render_native_scale=False, render_ascii=False):
    ascii = create_ascii_art(letters, gs_image)
    # print(str(ascii))
    width = len(gs_image[0])
    height = len(gs_image)

    image = Image.new('RGB', (width*font_size, height*font_size), (255,255,255))
    fnt = ImageFont.truetype(os.path.join(dev_folder, 'resources\\cour.ttf'), font_size)
    draw = ImageDraw.Draw(image)
    draw.multiline_text((0,0), print_image_representation(ascii), fill=0, font=fnt)
    
    if render_upscaled:
        image.save(os.path.join(training_folder, f'{render_name}_upscaled.jpg'))

    render = image.resize((width, height), Image.ANTIALIAS)
    
    if render_native_scale:
        render.save(os.path.join(training_folder, f'{render_name}_native.jpg'))
    return greyscale(render)

def create_ascii_art(letters: list, gs_image: list):
    gsm = create_greyscale_mapping(letters)
    ascii = map_to_ascii(gs_image, gsm)
    return ascii

# for performing testruns
def tst():
    letters = read_letters(os.path.join(dev_folder, "assets\\letters.ranked"))
    gs_image = scaled_convert_to_greyscale(os.path.join(dev_folder, "assets\\greyscale.jpg"), None, None)
    runner(letters, gs_image, 1)
    return

tst()