import csv
import pygame
import pygame.freetype
import time

# pygame setup
pygame.init()

disp_modes = pygame.display.list_modes()

screen = pygame.display.set_mode(disp_modes[0], pygame.FULLSCREEN, 0, 0, 1)

center_pos = pygame.Vector2(disp_modes[0][0] // 2, disp_modes[0][1] // 2)

pygame.display.set_caption('Stroop')

font = {
    'h1': pygame.freetype.SysFont(pygame.font.get_default_font(), 48, True),
    'p': pygame.freetype.SysFont(pygame.font.get_default_font(), 24)
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
            'col_char': row['colour'],
            'cond': int(row['cond']),
            'delay': float(row['delay']),
            'block': int(row['block']),
            'RT': -1,
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
    if exp_state > -1:
        cur_trial = cur_trial + 1
        if cur_trial >= len(exp_trials):
            running = False
        else:
            trial_timer = 0
            trial_showtime = 0
            trial_poll = False
    exp_state = exp_trials[cur_trial]['block']

def trial_pressed(keypress):
    global exp_trials
    press_time = time.perf_counter()
    if trial_poll:
        exp_trials[cur_trial]['RT'] = int(round((press_time - trial_showtime) * 1000))
        if keypress == exp_trials[cur_trial]['col_char']:
            exp_trials[cur_trial]['correct'] = True
    exp_continue()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((130,130,130))

    if exp_state == -1:
        write_text(readme, style='h1', pos = 'c')
    else:
        if trial_timer == 0:
            trial_timer = time.perf_counter()
        else:
            if (time.perf_counter() - trial_timer) * 1000 >= exp_trials[cur_trial]['delay']:
                write_text(exp_trials[cur_trial]['word'], colour=col_chars[exp_trials[cur_trial]['col_char']], style='h1', pos='c')
                if trial_poll == False:
                    trial_showtime = time.perf_counter()
                    trial_poll = True


    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False
        print('cond,RT,correct')
        for trial in exp_trials:
            print(trial['cond'], trial['RT'], trial['correct'], sep=',')
    else:
        if exp_state == -1:
            if keys[pygame.K_SPACE]:
                if not pressed:
                    pressed = True
                    exp_continue()
        else:
            if keys[pygame.K_r]:
                if not pressed:
                    pressed = True
                    trial_pressed('r')
            elif keys[pygame.K_g]:
                if not pressed:
                    pressed = True
                    trial_pressed('g')
            elif keys[pygame.K_b]:
                if not pressed:
                    pressed = True
                    trial_pressed('b')
            elif keys[pygame.K_y]:
                if not pressed:
                    pressed = True
                    trial_pressed('y')
            else:
                pressed = False

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()