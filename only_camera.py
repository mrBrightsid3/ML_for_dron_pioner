import cv2
import numpy as np
from pioneer_sdk import Camera
from get_coordinates import get_coordinates

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

# Connect to the drone camera
camera = Camera()

if __name__ == "__main__":
    while True:
        frame = camera.get_cv_frame()  # Get raw data
        x, y = get_coordinates(frame)
        print(f"x = {x}, y = {y}")
        cv2.imshow("video", frame)  # Show an image on the screen

        if cv2.waitKey(1) == 27:  # Exit if the ESC key is pressed
            break

    cv2.destroyAllWindows()  # Close all opened openCV windows
