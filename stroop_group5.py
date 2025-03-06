# config vars

generate_trials = True # if True will generate random trials at runtime else read file from trials_path
num_trials = 50 # number of trials to run if generating trials, ignored if reading trials from file
trials_path = 'data.csv'
fixation_time = 1000  # Duration of fixation cross (milliseconds), overrides delay if > 0
text_colour = 'white' # default text colour

colours = {
    'red': (230,38,0),
    'green': (38,230,0),
    'blue': (25,64,255),
    'yellow': (255,217,25),
    'white': (255,255,255),
    'black': (0,0,0)
}

key_colours = {
    'red': 'r',
    'green': 'g',
    'blue': 'b',
    'yellow': 'y'
}

readme = [
    {
        'text': 'You will be shown words written in different colours.',
        'colour': 'default'
    },
    {
        'text': 'Your task is to press the key that matches the colour of the word.',
        'colour': 'default'
    },
    {
        'text': 'red colour -> press R',
        'colour': 'red'
    }, 
    {
        'text': 'green colour -> press G',
        'colour': 'green'
    }, 
    {
        'text': 'blue colour -> press B',
        'colour': 'blue'
    }, 
    {
        'text': 'yellow colour -> press Y',
        'colour': 'yellow'
    },
    {
        'text': 'red -> press B',
        'colour': 'blue'
    },
    {
        'text': 'green -> press Y',
        'colour': 'yellow'
    },
    {
        'text': 'blue -> press R',
        'colour': 'red'
    },
    {
        'text': 'Good luck!',
        'colour': 'default'
    }
]

import csv
from datetime import datetime
import glob
import os
import pygame
import pygame.freetype
import sys
import time
import random

def write_text(text, colour='default', style='p', pos='c'):
    global text_colour
    if colour == 'default':
        colour = text_colour
    text_surf, text_rect = font[style].render(text, colours[colour])
    if pos == 'c':
        text_rect.center = center_pos
    else:
        text_rect.center = pos
    screen.blit(text_surf, text_rect)

def exp_continue():
    global exp_state, cur_trial, trial_timer, trial_showtime, trial_poll, running
    if exp_state > -1:
        cur_trial += 1
        if cur_trial >= len(exp_trials):  # Check if we've run out of trials
            screen.fill((0, 0, 0))
            write_text("Thank you for participating in this experiment!", style='h1')
            pygame.display.flip()
            time.sleep(3)  # Show the thank-you message for 3 seconds
            running = False
        else:
            trial_timer = 0
            trial_showtime = 0
            trial_poll = False
            exp_state = exp_trials[cur_trial]['block']
    else:
        countdown_timer() # Start countdown after pressing space
        exp_state = 0

def trial_pressed(keypress):
    global exp_trials
    press_time = time.perf_counter()
    if trial_poll:
        exp_trials[cur_trial]['RT'] = int(round((press_time - trial_showtime) * 1000))
        exp_trials[cur_trial]['keypress'] = chr(keypress)
        if chr(keypress) == key_colours[exp_trials[cur_trial]['colour']]:
            exp_trials[cur_trial]['correct'] = True
    exp_continue()

def countdown_timer(seconds=3):
    # Displays a countdown before the experiment starts.
    for i in range(seconds, 0, -1):
        screen.fill((0, 0, 0))
        write_text(f"Starting in {i}...", style='h1')
        pygame.display.flip()
        time.sleep(1)  # Pause for 1 second per number

    screen.fill((0, 0, 0))
    write_text("Get ready!", style='h1')
    pygame.display.flip()
    time.sleep(1)  # Brief pause before the experiment starts

def show_instructions(page=0):
    global center_pos, readme
    write_text(readme[page]['text'], readme[page]['colour'], 'h1')
    write_text('Press spacebar to continue...', pos=center_pos + (0,100))

def make_trial():
    trial = {
        'block': 1,
        'RT': 'NA',
        'keypress': 'NA',
        'correct': False
    }
    trial['word'] = random.choice(list(key_colours))
    if random.random() < .5:
        trial['colour'] = trial['word']
        trial['condition'] = 'congruent'
    else:
        trial['colour'] = random.choice(list(key_colours))
        trial['condition'] = 'incongruent'
    trial['delay'] = int(round(random.random() * 2000 + 1000))
    return trial

# pygame setup
pygame.init()

font = {
    'h1': pygame.freetype.SysFont(pygame.font.get_default_font(), 48, True),
    'p': pygame.freetype.SysFont(pygame.font.get_default_font(), 24),
    'trial': pygame.freetype.SysFont(pygame.font.get_default_font(), 96)
}

disp_flags = pygame.FULLSCREEN | pygame.SCALED
disp_modes = pygame.display.list_modes()
screen = pygame.display.set_mode(disp_modes[0], disp_flags, vsync=1)
pygame.display.set_caption('Stroop')

center_pos = pygame.Vector2(disp_modes[0][0] // 2, disp_modes[0][1] // 2)

pygame.mouse.set_visible(False)

running = True
instruct_state = 0
exp_state = -1
exp_trials = []
cur_trial = 0
trial_timer = 0
trial_showtime = 0
trial_poll = False

if generate_trials:
    for i in range(num_trials):
        exp_trials.append(make_trial())
else:
    with open('data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            trial = {
                'word': row['word'],
                'colour': row['colour'],
                'condition': row['condition'],
                'delay': int(row['delay']),
                'block': int(row['block']),
                'RT': 'NA',
                'keypress': 'NA',
                'correct': False
            }
            exp_trials.append(trial)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                if exp_state == -1:
                    if event.key == pygame.K_SPACE:
                        if instruct_state < len(readme) - 1:
                            instruct_state += 1
                        else:
                            exp_continue()
                else:
                    if event.key >= pygame.K_a and event.key <= pygame.K_z and trial_poll:
                        trial_pressed(event.key)

    # Clear the screen
    screen.fill((0, 0, 0))

    if running:
        if exp_state == -1:
            show_instructions(instruct_state)
        else:
            if trial_timer == 0:
                trial_timer = time.perf_counter()
                if fixation_time > 0:
                    exp_trials[cur_trial]['delay'] = fixation_time
            else:
                if (time.perf_counter() - trial_timer) * 1000 >= exp_trials[cur_trial]['delay']:
                    write_text(exp_trials[cur_trial]['word'], colour=exp_trials[cur_trial]['colour'], style='trial')
                    if trial_poll == False:
                        trial_showtime = time.perf_counter()
                        trial_poll = True
                else:
                    write_text("+", style='trial')

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()

session_prefix = 'session_' + datetime.today().strftime('%Y%m%d') + '_'
cur_session = len(glob.glob('./output/' + session_prefix + '*')) + 1

output_cols = ['word','colour','condition','delay','RT','keypress','correct','block']

with open(os.path.join('output', session_prefix + str(cur_session) + '.csv'), 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(output_cols)
    for trial in exp_trials:
        row_contents = []
        for col in output_cols:
            row_contents.append(trial[col])
        csvwriter.writerow(row_contents)

sys.exit()