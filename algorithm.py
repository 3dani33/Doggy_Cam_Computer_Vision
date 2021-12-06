"""Dog motion detection algorithm.

This contains the implementation of the computer vision algorithm for the 
project Doggy Cam. This module does no file handling and receives as input
images and returns the algorithm output of whether dog motion was detected."""

import numpy as np
import cv2 as cv

ALGORITHM_NAME = 'intensity'
ALGORITHM_VERSION = 'v2'

back_sub = cv.createBackgroundSubtractorMOG2(detectShadows=False)

threshold = 1385203
max_intens = 640 * 480 * 3 * 127        # frame_width x frame_height x number of cahnnels x max value per channel
max_valid_intens = max_intens * .045
# TODO soft code max intensity


def motion_detection(frame: np.array) -> bool:
    """This function is called for every image in a video and returns whether 
    dog motion and activity was detected for that frame."""

    back_sub_frame = back_sub.apply(frame, learningRate=-1)

    # background subtraction
    # sum all motion pixels
    sum = back_sub_frame.sum()

    result = False
    if(sum > threshold and sum < max_valid_intens):
        result = True
    #result = sum >= threshold
    # TODO: logging module might be better, so output for every frame can be turned off
    # print('threshold = ' + str(threshold))
    # print('intensity = ' + str(intensity))
    # print('above threshold? ' + str(check_threshold(intensity,threshold)))

    # return true
    return result, sum, back_sub_frame


def get_algorithm_version() -> str:
    """A string identifiying the current algorithm is returned. 

    The string contains the algorithm kind and a version, for example:
    dummy_v1 or simple_threshold_v2."""
    return '{}_{}'.format(ALGORITHM_NAME, ALGORITHM_VERSION)

