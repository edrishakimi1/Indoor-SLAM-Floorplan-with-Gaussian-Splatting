# mapping_splats.py
# This file builds a 3D map using simple Gaussian splats.

def load_trajectory(trajectory_path):
    """
    Load the camera poses from tracking.
    Return them as a list of 4x4 matrices.
    """
    pass


def backproject_depth_to_points(rgb, depth, intrinsics):
    """
    Convert depth image to 3D points in camera coordinates.
    Add color from the RGB image.
    Return Nx6 array: [x, y, z, r, g, b].
    """
    pass


def transform_points(points, pose):
    """
    Transform points from camera space to world space using camera pose.
    """
    pass


def cluster_points_into_splats(points):
    """
    Group nearby points using simple clustering (e.g., grid or k-means).
    For each cluster, compute:
      - mean position
      - scale (from covariance or bounding box)
      - average color
      - opacity
    Return a list of splat dictionaries.
    """
    pass


def save_splats_as_json(splats, output_path):
    """
    Save the Gaussian splats to a JSON file.
    """
    pass


def render_splat_preview(splats, camera_pose, output_path):
    """
    Simple CPU rendering:
      - project splats
      - sort by depth
      - alpha blend
    Save as an image.
    """
    pass


def run_mapping(data_path, traj_path, output_json, output_img):
    """
    Full mapping pipeline:
    - Load frames
    - Load trajectory
    - Backproject all depth frames
    - Transform points to world
    - Cluster into splats
    - Save splats and preview
    """
    pass


if __name__ == "__main__":
    run_mapping("../data/", "../results/trajectory.txt",
                "../results/splats.json",
                "../results/splat_preview.png")
