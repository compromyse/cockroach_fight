import cv2

import numpy as np

class Game:
    def __init__(self) -> None:
        # Open the webcame (0 is usually the default)
        self.cap = cv2.VideoCapture(0)

    def loop(self) -> None:
        while True:
            # Read frame
            ret, frame = self.cap.read()

            # If frame is not returned, break
            if not ret:
                break

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
            
            # Show frame
            cv2.imshow('Foot Tracking', frame)
            
            # Quit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()

    def stop(self) -> None:
        # Release captured webcam
        self.cap.release()
        
        # Destroy all CV2 Windows
        cv2.destroyAllWindows()

if __name__ == '__main__':
    game = Game()

    game.loop()