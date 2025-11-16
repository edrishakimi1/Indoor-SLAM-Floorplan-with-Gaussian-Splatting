# tracking.py
# This file handles camera pose estimation (tracking).
# It loads RGB-D frames, matches them, and prepares them for SLAM.
import numpy as np
import open3d as o3d

def read_assoc_file(file_path):
    """
    Read a TUM association file (rgb.txt or depth.txt).
    Each valid line looks like:
        timestamp filename

    Example:
        1305031102.175304 rgb/1305031102.175304.png

    Returns:
        List of (timestamp, filename)
    """

    pairs = []

    # open the file and read it line by line
    f = open(file_path, "r")
    for line in f:

        # skip comments or empty lines
        if line.strip() == "" or line.startswith("#"):
            continue

        # split into timestamp + filename
        parts = line.split()
        timestamp = float(parts[0])
        filename = parts[1]

        pairs.append((timestamp, filename))

    f.close()
    return pairs


def match_rgb_depth(rgb_list, depth_list):
    """
    Match each RGB frame with the closest depth frame in time.

    Why?
    - RGB and depth cameras do not take images at the exact same time.
    - We must find the depth frame whose timestamp is closest to the RGB timestamp.

    Input:
        rgb_list   = [(timestamp, rgb_file), ...]
        depth_list = [(timestamp, depth_file), ...]

    Output:
        matched = [(rgb_time, rgb_file, depth_file), ...]
    """

    matched = []

    for rgb_time, rgb_file in rgb_list:

        # assume the first depth frame is the best initially
        best_depth = depth_list[0]
        best_diff = abs(depth_list[0][0] - rgb_time)

        # search for a closer depth timestamp
        for depth_time, depth_file in depth_list:
            diff = abs(depth_time - rgb_time)

            if diff < best_diff:
                best_diff = diff
                best_depth = (depth_time, depth_file)

        # store matched RGB + deepest depth image
        matched.append((rgb_time, rgb_file, best_depth[1]))

    return matched


def load_rgbd_data(dataset_dir):
    """
    Load RGB and depth associations from the dataset directory.

    dataset_dir should contain:
        rgb.txt
        depth.txt
        rgb/
        depth/

    Returns:
        frames = list of dict:
            {
              "timestamp": ...,
              "rgb_path": ...,
              "depth_path": ...,
              "intrinsics": (fx, fy, cx, cy)
            }
    """

    print("Reading dataset from:", dataset_dir)

    # read associations
    rgb_list = read_assoc_file(dataset_dir + "/rgb.txt")
    depth_list = read_assoc_file(dataset_dir + "/depth.txt")

    print("RGB frames:", len(rgb_list))
    print("Depth frames:", len(depth_list))

    # match RGB and depth frames
    pairs = match_rgb_depth(rgb_list, depth_list)

    # camera intrinsics for freiburg1
    # these are fixed known values from the TUM dataset
    intrinsics = (517.3, 516.5, 318.6, 255.3)

    frames = []
    for ts, rgb_file, depth_file in pairs:
        frames.append({
            "timestamp": ts,
            "rgb_path": dataset_dir + "/" + rgb_file,
            "depth_path": dataset_dir + "/" + depth_file,
            "intrinsics": intrinsics
        })

    print("Matched pairs:", len(frames))
    return frames


def initialize_pose():
    """
    Return the starting camera pose.
    Usually this is a 4x4 identity matrix (camera starts at origin).
    """
    return np.eye(4)


def track_frame(prev_frame, curr_frame, prev_pose):
    """
    Estimate camera movement between two frames.

    You can implement:
      - feature matching + PnP
      - OR RGB-D ICP

    Returns:
        A 4x4 matrix representing the new camera pose.
    """
    fx, fy, cx, cy = prev_frame["intrinsics"]

    # --- 1. Load images ---
    rgb_prev  = o3d.io.read_image(prev_frame["rgb_path"])
    depth_prev = o3d.io.read_image(prev_frame["depth_path"])

    rgb_curr  = o3d.io.read_image(curr_frame["rgb_path"])
    depth_curr = o3d.io.read_image(curr_frame["depth_path"])

    # --- 2. Create RGBD frames ---
    rgbd_prev = o3d.geometry.RGBDImage.create_from_color_and_depth(
        rgb_prev, depth_prev, convert_rgb_to_intensity=False
    )

    rgbd_curr = o3d.geometry.RGBDImage.create_from_color_and_depth(
        rgb_curr, depth_curr, convert_rgb_to_intensity=False
    )

    # --- 3. Create intrinsics ---
    w = np.asarray(rgb_prev).shape[1]
    h = np.asarray(rgb_prev).shape[0]

    intr = o3d.camera.PinholeCameraIntrinsic(w, h, fx, fy, cx, cy)

    # --- 4. Create point clouds ---
    pcd_prev = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_prev, intr)
    pcd_curr = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_curr, intr)
    pcd_prev.estimate_normals()
    pcd_curr.estimate_normals()

    # --- 5. ICP Registration ---
    init_guess = np.eye(4)

    result = o3d.pipelines.registration.registration_icp(
        source=pcd_curr,
        target=pcd_prev,   # FIXED
        max_correspondence_distance=0.05,
        init=init_guess,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPlane()
    )

    T = result.transformation

    # --- 6. Update pose ---
    curr_pose = prev_pose @ T

    return curr_pose


def run_tracking(dataset_dir, output_path):
    """
    Main tracking flow:
    1. Load RGB-D frames
    2. Start with identity pose
    3. Loop through frames:
        - estimate motion
        - update pose
    4. Save poses to results file in TUM format
    """
    print("Loading data...")
    frames = load_rgbd_data(dataset_dir)

    print("Starting tracking on", len(frames), "frames")

    # --- 1. Prepare storage ---
    poses = []

    # --- 2. Initial camera pose (identity) ---
    pose = initialize_pose()
    poses.append((frames[0]["timestamp"], pose))

    # --- 3. Loop through all frame pairs ---
    for i in range(1, len(frames)):
        prev_frame = frames[i - 1]
        curr_frame = frames[i]

        print(f"Tracking frame {i}/{len(frames)-1}...")

        try:
            pose = track_frame(prev_frame, curr_frame, pose)
        except Exception as e:
            print("Tracking failed at frame", i, "error:", e)
            # keep previous pose to avoid crash
            poses.append((curr_frame["timestamp"], pose))
            continue

        poses.append((curr_frame["timestamp"], pose))

    # --- 4. Save results in TUM format ---
    print("Saving trajectory to:", output_path)
    with open(output_path, "w") as f:
        for ts, T in poses:
            # position
            tx, ty, tz = T[0, 3], T[1, 3], T[2, 3]

            # dummy quaternion rotation (no rotation)
            qx, qy, qz, qw = 0, 0, 0, 1

            f.write(f"{ts} {tx} {ty} {tz} {qx} {qy} {qz} {qw}\n")

    print("Tracking complete.")



if __name__ == "__main__":
    # change dataset path if needed
    run_tracking("data/rgbd_dataset_freiburg1_room", "results/trajectory.txt")
