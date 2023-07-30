import cv2
import numpy as np

import pygame
import random
import threading

from cockroach import Cockroach
from asteroid import Asteroid

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

class MyGame:
    def __init__(self) -> None:
        # Open the webcam (0 is usually the default)
        self.cap = cv2.VideoCapture(0)

        # Create a list to hold cockroaches
        self.cockroaches = []
        self.asteroids = []

        # Create the game screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Camera Feed and Cockroach Panel')

        # Track whether the Pygame window should be closed
        self.running = True

        # Create an event to signal the camera feed thread to stop
        self.stop_event = threading.Event()
    
    def spawn_objects(self):
        # Spawn a new cockroach randomly
        if len(self.cockroaches) < 5 and random.random() < 0.02:
            self.cockroaches.append(Cockroach())

        # Spawn a new asteroid randomly
        if len(self.asteroids) < 5 and random.random() < 0.02:
            self.asteroids.append(Asteroid())

    def move_objects(self):
        # Move cockroaches downwards and remove off-screen ones
        for cockroach in self.cockroaches:
            cockroach.move_down()
            if cockroach.y >= SCREEN_HEIGHT:
                self.cockroaches.remove(cockroach)

        # Move asteroid downwards and remove off-screen ones
        for asteroid in self.asteroids:
            asteroid.move_down()
            if asteroid.y >= SCREEN_HEIGHT:
                self.asteroids.remove(asteroid)
    
    def detect_collision(self, x, y):
        # Iterate through the list of cockroaches
        for cockroach in self.cockroaches:
            # Check if the detection rectangle intersects with the cockroach
            if x < cockroach.x < x + self.w and y < cockroach.y < y + self.h:
                # Remove the cockroach from the list
                self.cockroaches.remove(cockroach)
                return True
        return False

    def start_game(self):

        while not self.stop_event.is_set():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Set the stop event when the 'x' button is clicked
                    self.stop_event.set()

            self.spawn_objects()
            self.move_objects()

            # Read frame from the webcam
            ret, frame = self.cap.read()

            # If frame is not returned, break
            if not ret:
                break

            # Rotate the frame counter-clockwise by 90 degrees
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Convert frame from RGB to HSV, and define frame used for detection
            det_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define lower green and upper green            
            lower_green = np.array([60, 100, 100])
            upper_green = np.array([100, 255, 255])

            # Define green mask
            green_mask = cv2.inRange(det_frame, lower_green, upper_green)

            # Detect contours            
            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find largest contour
            largest_contour = max(contours, key=cv2.contourArea) if contours else None

            # If largest contour is present, draw a green rectangle
            if largest_contour is not None:
                x, y, self.w, self.h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + self.w, y + self.h), (0, 255, 0), 2)
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to Pygame surface
            frame_pygame = pygame.surfarray.make_surface(frame_rgb)

            # Draw the camera feed as the background
            self.screen.blit(frame_pygame, (0, 0))

            try:
                self.detect_collision(x,y)
            except:
                print('passing')
            # Draw the cockroach panel x,yon top of the camera feed
            for cockroach in self.cockroaches:
                cockroach.draw(self.screen)

            # Draw the cockroach panel on top of the camera feed
            for asteroid in self.asteroids:
                asteroid.draw(self.screen)

            # Update the display
            pygame.display.flip()

        # Release the captured webcam
        self.cap.release()

        # Destroy all CV2 Windows
        cv2.destroyAllWindows()

    def loop(self) -> None:
        # Start the webcam feed and cockroach panel in separate threads
        cockroach_thread = threading.Thread(target=self.start_game)
        cockroach_thread.start()

        while self.running:
            # Handle events for the Pygame window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Close the Pygame window
                    self.running = False

            # Quit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

        # Signal the camera feed thread to stop
        self.stop_event.set()

if __name__ == '__main__':
    game = MyGame()

    # Start the webcam feed and cockroach panel together
    game.loop()
