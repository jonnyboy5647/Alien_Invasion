import pygame
import time

pygame.init()
screen = pygame.display.set_mode((200, 200))
blue = (0, 0, 255)
screen.fill(blue)
pygame.display.flip()

# loop, otherwise python will stop running our game!
time.sleep(30)
