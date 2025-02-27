import csv
from datetime import datetime
import glob
import os
import pygame
import pygame.freetype
import sys
import time

# pygame setup
pygame.init()

disp_modes = pygame.display.list_modes()

screen = pygame.display.set_mode(disp_modes[0], pygame.FULLSCREEN, 0, 0, 1)

center_pos = pygame.Vector2(disp_modes[0][0] // 2, disp_modes[0][1] // 2)

pygame.display.set_caption('Stroop')
pygame.mouse.set_visible(False)

font = {
    'h1': pygame.freetype.SysFont(pygame.font.get_default_font(), 48, True),
    'p': pygame.freetype.SysFont(pygame.font.get_default_font(), 24),
    'trial': pygame.freetype.SysFont(pygame.font.get_default_font(), 108)
}

colours = {
    'red': (230,38,0),
    'green': (38,230,0),
    'blue': (25,64,255),
    'yellow': (255,217,25),
    'white': (255,255,255),
    'black': (0,0,0)
}

col_chars = {
    'r': 'red',
    'g': 'green',
    'b': 'blue',
    'y': 'yellow'
}

clock = pygame.time.Clock()
running = True
pressed = False
dt = 0

readme = 'Press spacebar to continue...'

def write_text(text, colour='black', style='p', pos='l'):
    text_surf, text_rect = font[style].render(text, colours[colour])
    if pos == 'c':
        text_rect.center = center_pos
    screen.blit(text_surf, text_rect)

exp_trials = []

with open('data.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        trial = {
            'word': row['word'],
            'colour': col_chars[row['colour']],
            'col_char': row['colour'],
            'cond': int(row['cond']),
            'delay': int(row['delay']),
            'block': int(row['block']),
            'RT': 'NA',
            'keypress': 'NA',
            'correct': False
        }
        exp_trials.append(trial)

exp_state = -1
cur_trial = 0
trial_timer = 0
trial_showtime = 0
trial_poll = False

def exp_continue():
    global exp_state
    global cur_trial
    global trial_timer
    global trial_showtime
    global trial_poll
    global running
    if exp_state > -1:
        cur_trial += 1
        if cur_trial >= len(exp_trials):
            running = False
        else:
            trial_timer = 0
            trial_showtime = 0
            trial_poll = False
            exp_state = exp_trials[cur_trial]['block']
    else:
        exp_state += 1

def trial_pressed(keypress):
    global exp_trials
    press_time = time.perf_counter()
    if trial_poll:
        exp_trials[cur_trial]['RT'] = int(round((press_time - trial_showtime) * 1000))
        exp_trials[cur_trial]['keypress'] = chr(keypress)
        if chr(keypress) == exp_trials[cur_trial]['col_char']:
            exp_trials[cur_trial]['correct'] = True
    exp_continue()


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

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((130,130,130))

    if exp_state == -1:
        write_text(readme, style='h1', pos = 'c')
    else:
        if trial_timer == 0:
            trial_timer = time.perf_counter()
        else:
            if (time.perf_counter() - trial_timer) * 1000 >= exp_trials[cur_trial]['delay']:
                write_text(exp_trials[cur_trial]['word'], colour=col_chars[exp_trials[cur_trial]['col_char']], style='trial', pos='c')
                if trial_poll == False:
                    trial_showtime = time.perf_counter()
                    trial_poll = True

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