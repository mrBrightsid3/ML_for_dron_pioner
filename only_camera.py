import cv2
import numpy as np
from pioneer_sdk import Camera

# Connect to the drone camera
camera = Camera()

if __name__ == "__main__":
    while True:
        frame = camera.get_cv_frame()  # Get raw data
        cv2.imshow("video", frame)  # Show an image on the screen

        if cv2.waitKey(1) == 27:  # Exit if the ESC key is pressed
            break

    cv2.destroyAllWindows()  # Close all opened openCV windows
