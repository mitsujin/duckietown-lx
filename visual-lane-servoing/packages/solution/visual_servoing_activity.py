from typing import Tuple

import numpy as np
import cv2


def get_steer_matrix_left_lane_markings(shape: Tuple[int, int]) -> np.ndarray:
    """
    Args:
        shape:              The shape of the steer matrix.

    Return:
        steer_matrix_left:  The steering (angular rate) matrix for Braitenberg-like control
                            using the masked left lane markings (numpy.ndarray)
    """

    # TODO: implement your own solution here
    w = shape[1]
    h = shape[0]

    #steer_matrix_left = np.ones(shape=shape, dtype=np.float32)
    steer_matrix_left = np.full(shape, -1, dtype=np.float32)
    #steer_matrix_left[0:h, 0:w//2] = -1

    # ---
    return steer_matrix_left


def get_steer_matrix_right_lane_markings(shape: Tuple[int, int]) -> np.ndarray:
    """
    Args:
        shape:               The shape of the steer matrix.

    Return:
        steer_matrix_right:  The steering (angular rate) matrix for Braitenberg-like control
                             using the masked right lane markings (numpy.ndarray)
    """

    w = shape[1]
    h = shape[0]

    #steer_matrix_right = np.ones(shape=shape, dtype=np.float32)
    steer_matrix_right = np.full(shape, 1, dtype=np.float32)
    #steer_matrix_right[0:h, 0:w//2] = 1
    #steer_matrix_right[0:h, (w//2):(w)] = -1
    
    # ---
    return steer_matrix_right


def detect_lane_markings(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Args:
        image: An image from the robot's camera in the BGR color space (numpy.ndarray)
    Return:
        mask_left_edge:   Masked image for the dashed-yellow line (numpy.ndarray)
        mask_right_edge:  Masked image for the solid-white line (numpy.ndarray)
    """
    h, w, _ = image.shape
    sigma = 5 
    threshold = [[60.0]]

    imgrgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imghsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img_gaussian_filter = cv2.GaussianBlur(img, (0,0), sigma)
    sobelx = cv2.Sobel(img_gaussian_filter, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(img_gaussian_filter, cv2.CV_64F, 0, 1)
    Gmag = np.sqrt(sobelx*sobelx + sobely*sobely)

    mask_mag = (Gmag > threshold)

    white_lower_hsv = np.array([0, 0, 190.85])         # CHANGE ME
    white_upper_hsv = np.array([179, 56.1, 255])   # CHANGE ME
    yellow_lower_hsv = np.array([25.159, 99.45, 114.75])        # CHANGE ME
    yellow_upper_hsv = np.array([27.84, 255, 255])  # CHANGE ME

    mask_white = cv2.inRange(imghsv, white_lower_hsv, white_upper_hsv)
    mask_yellow = cv2.inRange(imghsv, yellow_lower_hsv, yellow_upper_hsv)

    mask_left = np.ones(sobelx.shape)
    mask_left[:, int(np.floor(w/2)):w+1] = 0
    mask_right = np.ones(sobelx.shape)
    mask_right[:, 0:int(np.floor(w/2))] = 0

    mask_sobelx_pos = (sobelx > 0)
    mask_sobelx_neg = (sobelx < 0)
    mask_sobely_pos = (sobely > 0)
    mask_sobely_neg = (sobely < 0)

    mask_left_edge = mask_left * mask_mag * mask_sobelx_neg * mask_sobely_neg * mask_yellow
    mask_right_edge = mask_right * mask_mag * mask_sobelx_pos * mask_sobely_neg * mask_white

    return mask_left_edge, mask_right_edge
