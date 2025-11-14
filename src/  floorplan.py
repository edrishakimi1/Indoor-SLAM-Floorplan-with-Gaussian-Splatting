# floorplan.py
# This file extracts a 2D floorplan from the 3D map.

def load_splats(splats_path):
    """
    Load Gaussian splats from JSON.
    Return their 3D centers.
    """
    pass


def remove_floor_and_ceiling(points, floor_height, ceiling_height):
    """
    Filter out points below floor_height and above ceiling_height.
    Keep only wall and structure points.
    """
    pass


def project_points_to_2d(points):
    """
    Drop the Z coordinate.
    Convert 3D to 2D ground plane (x, y).
    """
    pass


def create_occupancy_grid(points, resolution):
    """
    Convert 2D points to a grid map:
      - Mark free/wall cells
    Return a 2D numpy array.
    """
    pass


def clean_grid(grid):
    """
    Apply morphological filtering to remove noise.
    """
    pass


def extract_walls_hough(grid):
    """
    Use Hough Transform or line fitting to detect major walls.
    Return line segments.
    """
    pass


def save_floorplan(grid, output_image):
    """
    Save grid as floorplan image.
    """
    pass


def save_walls_geojson(walls, output_path):
    """
    Save wall line segments in GeoJSON format.
    """
    pass


def run_floorplan(splats_path, output_floorplan, output_walls):
    """
    Main floorplan pipeline:
    - Load splats
    - Remove floor and ceiling
    - Project to 2D
    - Build occupancy grid
    - Extract walls
    - Save results
    """
    pass


if __name__ == "__main__":
    run_floorplan("../results/splats.json",
                  "../results/floorplan.png",
                  "../results/walls.geojson")
