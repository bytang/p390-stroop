# config vars

fixation_time = 1000  # Duration of fixation cross (milliseconds)

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

readme = 'Press spacebar to continue...'

import csv
from datetime import datetime
import glob
import os
import pygame
import pygame.freetype
import sys
import time

def write_text(text, colour='black', style='p', pos='c'):
    text_surf, text_rect = font[style].render(text, colours[colour])
    if pos == 'c':
        text_rect.center = center_pos
    screen.blit(text_surf, text_rect)

def exp_continue():
    global exp_state
    global cur_trial
    global trial_timer
    global trial_showtime
    global trial_poll
    global running
    if exp_state > -1:
        cur_trial += 1
        if cur_trial >= len(exp_trials):  # Check if we've run out of trials
            screen.fill((0, 0, 0))
            write_text("Thank you for participating in this experiment!", colour='white', style='h1', pos='c')
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
        exp_state += 1

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
    """Displays a countdown before the experiment starts."""
    for i in range(seconds, 0, -1):
        screen.fill((0, 0, 0))
        write_text(f"Starting in {i}...", colour='white', style='h1')
        pygame.display.flip()
        time.sleep(1)  # Pause for 1 second per number

    screen.fill((0, 0, 0))
    write_text("Get ready!", colour='white', style='h1')
    pygame.display.flip()
    time.sleep(1)  # Brief pause before the experiment starts

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
exp_state = -1
exp_trials = []
cur_trial = 0
trial_timer = 0
trial_showtime = 0
trial_poll = False

with open('data.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        trial = {
            'word': row['word'],
            'colour': row['colour'],
            'cond': int(row['cond']),
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
                        exp_continue()
                else:
                    if event.key >= pygame.K_a and event.key <= pygame.K_z and trial_poll:
                        trial_pressed(event.key)

    # Clear the screen
    screen.fill((0, 0, 0))

    if running:
        if exp_state == -1:
            write_text(readme, colour='white', style='h1')
        else:
            if trial_timer == 0:
                trial_timer = time.perf_counter()
            else:
                delay = 0
                if fixation_time > 0:
                    delay = fixation_time
                else:
                    delay = exp_trials[cur_trial]['delay']
                if (time.perf_counter() - trial_timer) * 1000 >= delay:
                    write_text(exp_trials[cur_trial]['word'], colour=exp_trials[cur_trial]['colour'], style='trial')
                    if trial_poll == False:
                        trial_showtime = time.perf_counter()
                        trial_poll = True
                else:
                    write_text("+", colour='white', style='trial')

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()

session_prefix = 'session_' + datetime.today().strftime('%Y%m%d') + '_'
cur_session = len(glob.glob('./output/' + session_prefix + '*')) + 1

output_cols = ['word','colour','cond','delay','RT','keypress','correct','block']

with open(os.path.join('output', session_prefix + str(cur_session) + '.csv'), 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(output_cols)
    for trial in exp_trials:
        row_contents = []
        for col in output_cols:
            if col == 'RT' and trial[col] == -1:
                    row_contents.append('NA')
            else:
                row_contents.append(trial[col])
        csvwriter.writerow(row_contents)

sys.exit()