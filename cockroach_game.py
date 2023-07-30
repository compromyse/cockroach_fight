import pygame
import random

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Load cockroach image
cockroach_image = pygame.image.load('res/cockroach.png')

class Cockroach:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = random.randint(0, SCREEN_HEIGHT - 40)
        self.speed_x = random.randint(1, 5)

    def move(self):
        self.x -= self.speed_x

    def draw(self, screen):
        screen.blit(cockroach_image, (self.x, self.y))

def main():
    # Create the game screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Cockroach Spawning and Movement')

    # Create a list to hold cockroaches
    cockroaches = []

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawn a new cockroach randomly
        if len(cockroaches) < 5 and random.random() < 0.02:
            cockroaches.append(Cockroach())

        # Move cockroaches and remove off-screen ones
        for cockroach in cockroaches:
            cockroach.move()
            if cockroach.x <= -40:
                cockroaches.remove(cockroach)

        # Draw everything on the screen
        
        for cockroach in cockroaches:
            cockroach.draw(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
