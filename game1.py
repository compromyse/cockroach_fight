import cv2
import numpy as np
import pygame
import random
import threading
from cockroach_game import Cockroach

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Load cockroach image
cockroach_image = pygame.image.load('res/cockroach.png')

class MyGame:
    def __init__(self) -> None:
        # Open the webcam (0 is usually the default)
        self.cap = cv2.VideoCapture(0)

        # Create the game screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Camera Feed and Cockroach Panel')

    def run_cockroach_game(self):
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
            self.screen.fill((255, 255, 255))  # Fill the screen with white
            for cockroach in cockroaches:
                cockroach.draw(self.screen)

            # Update the display
            pygame.display.flip()

    def loop(self) -> None:
        # Start the webcam feed and cockroach panel in separate threads
        cockroach_thread = threading.Thread(target=self.run_cockroach_game)
        cockroach_thread.start()

        while True:
            # Read frame from the webcam
            ret, frame = self.cap.read()

            # If frame is not returned, break
            if not ret:
                break

            # Convert frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to Pygame surface
            frame_pygame = pygame.surfarray.make_surface(frame_rgb)

            # Blit the camera feed onto the Pygame screen
            self.screen.blit(frame_pygame, (80, 60))

            # Update the display
            pygame.display.flip()

            # Quit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()

    def stop(self) -> None:
        # Release the captured webcam
        self.cap.release()

        # Destroy all CV2 Windows
        cv2.destroyAllWindows()

if __name__ == '__main__':
    game = MyGame()

    # Start the webcam feed and cockroach panel together
    game.loop()
