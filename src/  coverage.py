# coverage.py
# This file computes how much of the room was scanned.

def initialize_coverage_grid(width, height, resolution):
    """
    Create an empty observation count grid.
    """
    pass


def update_coverage_with_frame(points, grid):
    """
    For each 3D (or 2D) point, find the grid cell it hits.
    Increase observation count.
    """
    pass


def compute_coverage_metrics(grid, threshold):
    """
    Calculate:
      - total number of cells
      - number of cells with count >= threshold
      - percentage coverage
    """
    pass


def save_coverage_heatmap(grid, output_path):
    """
    Save coverage grid as a heatmap image.
    """
    pass


def save_metrics_json(metrics, output_path):
    """
    Save dictionary of metrics to JSON.
    """
    pass


def run_coverage(points_2d, output_heatmap, output_metrics):
    """
    Full coverage pipeline:
    - Build grid
    - Update grid with all frames
    - Compute metrics
    - Save heatmap and metrics JSON
    """
    pass


if __name__ == "__main__":
    run_coverage(None, "../results/coverage_heatmap.png",
                 "../results/metrics.json")
