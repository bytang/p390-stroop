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
    'yellow': (255,217,25)
}

clock = pygame.time.Clock()
running = True
pressed = False
pressTime = time.perf_counter()
dt = 0

readme = 'Press spacebar to continue...'

def write_text(text, colour = (0, 0, 0), style = 'p', pos = 'l'):
    text_surf, text_rect = font[style].render(text, colour)
    if pos == 'c':
        text_rect.center = center_pos
    screen.blit(text_surf, text_rect)
    

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((130,130,130))

    # font.render_to(screen, center_pos, str(round((time.perf_counter() - pressTime) * 1000)), (255, 255, 255))

    write_text(readme, style = 'h1', pos = 'c')

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False
    elif keys[pygame.K_SPACE]:
        if not pressed:
            pressTime = time.perf_counter()
            pressed = True
    else:
        pressed = False

    # flip() the display to put your work on screen
    clock.tick(1000)
    pygame.display.flip()

pygame.quit()