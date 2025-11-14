# Indoor SLAM & Floorplan (with Gaussian Splatting)
Status: Work in Progress

This project takes a short indoor RGB-D sequence and produces:
- A camera trajectory (poses over time)
- A 3D map using lightweight Gaussian splats
- A 2D floorplan (walls and free space)
- An optional coverage/confidence heatmap

The goal is to create a simple and clear SLAM pipeline, not a full research-grade system.

---

## Project Structure
```
project/
  data/        # RGB-D dataset (TUM format)
  src/         # Code for tracking, mapping, floorplan, coverage
  results/     # Output files (trajectory, splats, floorplan, heatmap)
```

---

## Pipeline Overview

### 1. Tracking
- Estimate camera pose for every frame.
- Use feature-based PnP or RGB-D ICP.
- Output: results/trajectory.txt

### 2. Mapping (Gaussian Splats)
- Fuse 3D points from all frames.
- Cluster points into simple Gaussian splats.
- Basic CPU-based splat rendering.
- Outputs: results/splats.json, results/splat_preview.png

### 3. 2D Floorplan
- Remove floor and ceiling.
- Create a 2D occupancy grid.
- Extract wall lines (Hough transform or line fitting).
- Outputs: results/floorplan.png, results/walls.geojson

### 4. Coverage / Confidence (Optional)
- Count how many times each grid cell is observed.
- Generate a 2D heatmap of scan coverage.
- Outputs: results/coverage_heatmap.png, results/metrics.json

---

## Tools and Libraries
- Python
- NumPy
- OpenCV
- Open3D
- SciPy

---

## Dataset
Using the TUM RGB-D dataset (example: freiburg1_room):  
https://cvg.cit.tum.de/rgbd/dataset/freiburg1/

Place the downloaded dataset inside the `data/` folder.

---

## Work in Progress
- [ ] Implement tracking
- [ ] Build Gaussian splat mapping
- [ ] Extract 2D floorplan
- [ ] Add coverage heatmap
- [ ] Add evaluation metrics
- [ ] Improve visualization

This README will be updated as the project continues.

---

## Author
Edris Hakimi
