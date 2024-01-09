import pygame
from sys import exit
from classes import Game
from json import load


params = load(open("params.json", 'r'))


pygame.init()

width, height = params["width"], params["height"]
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation alfa version")
background_color = (0,0,0)


game = Game(screen=screen, n_patrols=params["n_patrols"],n_cameras=params["n_cameras"],n_ii_per_second=params["mean_illegal_imigrants_respawn_per_second"])


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    game.go()

    pygame.display.flip()
    pygame.time.Clock().tick(30)



print(round(game.counter_finished_imigrants*100/game.counter_spawn_illegal_imigrants), "% of all illegal immigrants crossed the border", sep='')
pygame.quit()
exit()

