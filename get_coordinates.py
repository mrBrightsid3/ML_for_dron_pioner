import cv2
from pioneer_sdk import Pioneer, Camera
import numpy as np


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)


def get_coordinates(frame):
    corners, ids, rejected = aruco_detector.detectMarkers(frame)
    if np.all(ids is not None):
        x_center = int(
            (
                corners[0][0][0][0]
                + corners[0][0][1][0]
                + corners[0][0][2][0]
                + corners[0][0][3][0]
            )
            // 4
        )
        y_center = int(
            (
                corners[0][0][0][1]
                + corners[0][0][1][1]
                + corners[0][0][2][1]
                + corners[0][0][3][1]
            )
            // 4
        )
        return x_center, y_center
