import os
import time

import pygame

PID_FILE = os.path.expanduser('~/.pi-board-rumbler/pid.txt')

pygame.display.init()
# successes, failures = pygame.init()
# print("{0} successes and {1} failures".format(successes, failures))
pygame.mouse.set_visible(0)
screen = pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()
FPS = 30  # Frames per second.

pygame.font.init()  # you have to call this at the start,
# if you want to use this module.

# Comic sans deserves to be loved
myfont = pygame.font.SysFont('Comic Sans MS', 20)
textsurfaceStatus = myfont.render("Loading", False, (255, 255, 255))
textsurfaceAction = myfont.render('Press A to toggle, Select to quit', False, (255, 255, 255))


def is_running():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as myfile:
            pid = myfile.read()
            if bool(pid):
                try:
                    os.kill(int(pid), 0)
                except OSError:
                    return False
                else:
                    return True
    else:
        return False


def update_ui():
    global textsurfaceStatus
    running = is_running()
    if running:
        statusText = 'Rumble is active'
    else:
        statusText = 'Rumble is not active'
    textsurfaceStatus = myfont.render(statusText, False, (255, 255, 255))


def toggle():
    running = is_running()
    if running:
        os.system("/bin/sh ./stop-rumble-listener.sh")
    else:
        os.system("/bin/sh ./start-rumble-listener.sh")
    time.sleep(0.2)
    update_ui()


update_ui()

RG350_A_KEYCODE = 306

loop = True
while loop:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_POWER or event.key == pygame.K_ESCAPE:
                loop = False
            elif event.key == RG350_A_KEYCODE or event.key == pygame.K_RETURN:
                toggle()

    screen.fill((0, 0, 0))
    screen.blit(textsurfaceStatus, (25, 50))
    screen.blit(textsurfaceAction, (25, 100))
    pygame.display.flip()

pygame.display.quit()
quit()
