import cv2
import numpy as np
import pygame
import random
import threading

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

def run_cockroach_game():
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
        screen.fill((255, 255, 255))  # Fill the screen with white
        for cockroach in cockroaches:
            cockroach.draw(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()

class Game:
    def __init__(self) -> None:
        # Open the webcam (0 is usually the default)
        self.cap = cv2.VideoCapture(0)

    def loop(self) -> None:
        while True:
            # Read frame
            ret, frame = self.cap.read()

            # If frame is not returned, break
            if not ret:
                break

            # Convert frame from RGB to HSV and define frame used for detection
            det_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define lower green and upper green            
            lower_green = np.array([60, 100, 100])
            upper_green = np.array([100, 255, 255])

            # Define green mask            
            green_mask = cv2.inRange(det_frame, lower_green, upper_green)

            # Detect contours            
            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea) if contours else None

            # If the largest contour is present, draw a green rectangle
            if largest_contour is not None:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Show the frame
            cv2.imshow('Foot Tracking', frame)
            
            # Quit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()

    def stop(self) -> None:
        # Release the captured webcam
        self.cap.release()
        
        # Destroy all CV2 Windows
        cv2.destroyAllWindows()

if __name__ == '__main__':
    game = Game()

    # Start the cockroach game in a separate thread
    cockroach_thread = threading.Thread(target=run_cockroach_game)
    cockroach_thread.start()

    # Start the webcam feed and foot tracking loop
    game.loop()