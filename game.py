import cv2
import numpy as np
import pygame
import random
import threading
from cockroach_game import Cockroach

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 802
SCREEN_HEIGHT = 601

# Load cockroach image
cockroach_image = pygame.image.load('res/cockroach.png')

class MyGame:
    def __init__(self) -> None:
        # Open the webcam (0 is usually the default)
        self.cap = cv2.VideoCapture(0)

        # Create the game screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Camera Feed and Cockroach Panel')

        # Track whether the Pygame window should be closed
        self.running = True

        # Create an event to signal the camera feed thread to stop
        self.stop_event = threading.Event()

    def run_cockroach_game(self):
        # Create a list to hold cockroaches
        cockroaches = []

        while not self.stop_event.is_set():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Set the stop event when the 'x' button is clicked
                    self.stop_event.set()

            # Spawn a new cockroach randomly
            if len(cockroaches) < 5 and random.random() < 0.02:
                cockroaches.append(Cockroach())

            # Move cockroaches downwards and remove off-screen ones
            for cockroach in cockroaches:
                cockroach.move_down()
                if cockroach.y >= SCREEN_HEIGHT:
                    cockroaches.remove(cockroach)

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
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to Pygame surface
            frame_pygame = pygame.surfarray.make_surface(frame_rgb)

            # Draw the camera feed as the background
            self.screen.blit(frame_pygame, (80, 60))

            # Draw the cockroach panel on top of the camera feed
            for cockroach in cockroaches:
                cockroach.draw(self.screen)

            # Update the display
            pygame.display.flip()

        # Release the captured webcam
        self.cap.release()

        # Destroy all CV2 Windows
        cv2.destroyAllWindows()

    def loop(self) -> None:
        # Start the webcam feed and cockroach panel in separate threads
        cockroach_thread = threading.Thread(target=self.run_cockroach_game)
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
