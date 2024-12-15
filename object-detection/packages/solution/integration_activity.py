from typing import Tuple
import numpy as np


def DT_TOKEN() -> str:
    # TODO: change this to your duckietown token
    dt_token = "dt2-5wjpkjyNDVkVSh5zZ1XnnAMCF5H6Rwyf1KCAFsNcQFXzuR62haMtECrUjoRbxFw3rnYGamyDREMNdGJuS-43dzqWFnWd8KBa1yev1g3UKnzVxZkkTbfdqoJj54FagXAjWWdm5cSHehNVPBpF8z3H"
    return dt_token


def MODEL_NAME() -> str:
    # TODO: change this to your model's name that you used to upload it on google colab.
    # if you didn't change it, it should be "yolov5n"
    return "yolov5n"


def NUMBER_FRAMES_SKIPPED() -> int:
    # TODO: change this number to drop more frames
    # (must be a positive integer)
    return 10


def filter_by_classes(pred_class: int) -> bool:
    """
    Remember the class IDs:

        | Object    | ID    |
        | ---       | ---   |
        | Duckie    | 0     |
        | Cone      | 1     |
        | Truck     | 2     |
        | Bus       | 3     |


    Args:
        pred_class: the class of a prediction
    """
    # Right now, this returns True for every object's class
    # TODO: Change this to only return True for duckies!
    # In other words, returning False means that this prediction is ignored.
    if pred_class == 0: return True
    return False


def filter_by_scores(score: float) -> bool:
    """
    Args:
        score: the confidence score of a prediction
    """
    # Right now, this returns True for every object's confidence
    # TODO: Change this to filter the scores, or not at all
    # (returning True for all of them might be the right thing to do!)
    return True


def filter_by_bboxes(bbox: Tuple[int, int, int, int]) -> bool:
    area = np.abs(bbox[2] - bbox[0]) * np.abs(bbox[1] - bbox[3])

    width = 416

    if (bbox[2] < 200 and bbox[3] < 200): return False
    if area < 1000: return False

    """
    Args:
        bbox: is the bounding box of a prediction, in xyxy format
                This means the shape of bbox is (leftmost x pixel, topmost y, rightmost x, bottommost y)
    """
    # TODO: Like in the other cases, return False if the bbox should not be considered.
    return True
