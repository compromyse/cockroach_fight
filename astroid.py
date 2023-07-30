import pygame
import random

# Load asteroid image
asteroid_image = pygame.image.load('res/asteroid.png')

class Asteroid:
    def __init__(self):
        self.x = random.randint(80, 800)  # Random x position within the screen width
        self.y = 60  # Starting y position at the top
        self.speed_y = random.randint(1, 3)  # Random downward speed

    def move_down(self):
        self.y += self.speed_y

    def draw(self, screen):
        screen.blit(asteroid_image, (self.x, self.y))
