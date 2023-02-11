import os
from random import randint
import pygame
from nim import Nim
from main_screen import MainScreen

WIDTH, HEIGHT = 900, 720 

GOLF_BALL_SPRITE = pygame.image.load(
    os.path.join('assets', 'golf-ball.png'))

def main(): 
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Nimulator')
    # game = Nim([10, 5, 7, 2, 1, 4, 6, 8, 3, 9])
    game = Nim(list([randint(1, 10) for _ in range(0, 10)]), 
        list([randint(1, 10) for _ in range(0, 10)]))
    screen = MainScreen(GOLF_BALL_SPRITE , game)
    while screen: 
        for event in pygame.event.get(): 
            if screen: 
                screen = screen.run(event)
        if screen: 
            screen.draw(window)
    pygame.quit() 

if __name__ == '__main__': 
    main()