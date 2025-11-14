# tracking.py
# This file handles camera pose estimation (tracking)
# It loads RGB-D frames, computes motion, and saves trajectory.

def load_rgbd_data(data_path):
    """
    Load RGB images, depth images, and camera intrinsics from the dataset.
    Return them in a simple list or dictionary.
    """
    pass


def initialize_pose():
    """
    Return the starting camera pose (usually identity matrix).
    """
    pass


def track_frame(prev_frame, curr_frame, prev_pose):
    """
    Estimate camera motion between two frames.
    Use either:
      - feature matching + PnP
      - or RGB-D ICP
    
    Return: 4x4 pose matrix for the current frame.
    """
    pass


def run_tracking(data_path, output_path):
    """
    Main tracking function:
    - Load all frames
    - Loop through frames
    - Estimate pose for each frame
    - Save poses in TUM format to output_path
    """
    pass


if __name__ == "__main__":
    # Example run code (edit later)
    run_tracking("../data/", "../results/trajectory.txt")
