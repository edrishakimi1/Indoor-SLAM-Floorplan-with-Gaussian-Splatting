# math_utils.py
# Basic math functions (poses, transformations)

import numpy as np

def identity_pose():
    """
    Return a 4x4 identity matrix.
    """
    return np.eye(4)


def pose_to_tum_format(pose, timestamp):
    """
    Convert 4x4 pose matrix to TUM trajectory line.
    """
    pass


def transform_points(points, pose):
    """
    Apply a 4x4 pose transform to a set of points.
    """
    pass
