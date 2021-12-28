from math import pi
import threading
from random import randint

from PIL.ImageFont import TransposedFont
from trainer import render_ascii

# evaluates the fitness of own letter based on the immiedeately surrounding pixels
class LetterEvaluator:
    letter = ''
    pixel_ws = []
    pixel_intervals = []

    training_rate = 1 # we want to train at a rate relative to the magnitude of the error value (255 is max greyscale value)
    w_training_rate = 1/(255 * 10)

    # pixels are passed on top left -> bottom right
    def __init__(self, letter: str, letter_fitness: list, pixel_intervals: list):
        self.letter = letter
        self.pixel_ws = letter_fitness
        self.pixel_intervals = pixel_intervals
        
    # return the new error for this example after training
    def train(self, pixels: list):
        target = pixels[4]
        result = render_ascii([[self.letter]], [[target]], self.letter + "_training")
        self.update(target - result[0][0])
        return target - result[0][0]

    def update(self, err: int):
        pixel_ws = self.pixel_ws
        pixel_intervals = self.pixel_intervals
        idx = 0
        for pixel_w in pixel_ws:
            lower = pixel_intervals[idx * 2]
            upper = pixel_intervals[idx * 2 + 1]

            pixel_ws[idx] = pixel_w - err * self.w_training_rate
            if err > 0:
                pixel_intervals[idx * 2] += self.training_rate
                pixel_intervals[idx * 2 + 1] += self.training_rate
            elif err < 0:
                pixel_intervals[idx * 2] -= self.training_rate
                pixel_intervals[idx * 2 + 1] -= self.training_rate
                
            idx += 1

    def mutate(self):
        element = randint(0,1)
        direction = randint(0,1)
        pixel = randint(0,8)
        interval_change = randint(0,len(self.pixel_intervals) - 1)
        
        if element > 0:
            if direction > 0:
                self.pixel_ws[pixel] = self.pixel_ws[pixel] + self.w_training_rate
            else:
                self.pixel_ws[pixel] = self.pixel_ws[pixel] - self.w_training_rate
        else:
            if direction > 0:
                self.pixel_intervals[interval_change] += 1
            else:
                self.pixel_intervals[interval_change] -=1

            
    def evaluate_fitness(self, pixels:list):
        fitness = 0
        pixel_ws = self.pixel_ws
        pixel_intervals = self.pixel_intervals
        idx = 0
        for pixel in pixels:
            if pixel > pixel_intervals[idx*2] and pixel < pixel_intervals[idx*2 + 1]:
                fitness += 1 * pixel_ws[idx]
            idx += 1
        return fitness



# Chooses a letter based on a set of pixels containing the one we want and its 8 immediate neighbours
class LetterPicker:
    letters = []
    letter_evalueators: dict[str, LetterEvaluator] = {}

    def __init__(self, letter_fitts:dict):
        
        for letter in letter_fitts:
            self.letters.append(letter)
            self.letter_evaluators[letter] = LetterEvaluator(letter, letter_fitts[letter])
    
    def train(self, pixels: list):
        letter_evals:dict[str, LetterEvaluator] = self.letter_evaluators

        # get the letter evaluators to guess their letters fitness
        evals = {}
        scores = {}
        best_score = 9999
        best_letter = ''
        for letter in letter_evals:
            evals[letter] = letter_evals[letter].evaluate_fitness(pixels)
            # render the target pixel to see how close the evaluators were
            scores[letter] = abs(pixels[4] - render_ascii([[letter]],[[pixels[4]]])[0][0])
            if scores[letter] < best_score:
                best_score = scores[letter]
                best_letter = letter
        
        # make the evaluators that did poorly train
        for letter in letter_evals:
            if letter != best_letter and eval[letter] > eval[best_letter]:
                trainee = letter_evals[letter]
                mutation = LetterEvaluator(trainee.letter, trainee.pixel_ws.copy(), trainee.pixel_intervals.copy())
                mutation.mutate()
                e_t = scores[letter]
                e_m = scores[letter]
                for iter in range(100):
                    e_t = trainee.train(pixels)
                    e_m = mutation.train(pixels)
                
                if abs(e_m) < abs(e_t):
                    letter_evals[letter] = mutation


        
        

        
