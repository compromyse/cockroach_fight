import pygame
import random


class Cockroach:
    def __init__(self):
        self.x = random.randint(80, 800)  # Random x position within the screen width
        self.y = 60  # Starting y position at the top
        self.speed_y = random.randint(1, 5)  # Random downward speed

        self.width = 95
        self.height = 113

        # Load cockroach image
        self.cockroach_image = pygame.image.load('res/cockroach.png')

    def move_down(self):
        self.y += self.speed_y

    def draw(self, screen):
        screen.blit(self.cockroach_image, (self.x, self.y))
