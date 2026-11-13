
import os
import numpy as np
import rasterio
from rasterio.enums import Resampling
from PIL import Image

INPUT = "data/nasa/mola-global-dem/mola128_mola64_merge_90Nto90S_SimpleC_clon0.tif"
OUTPUT = "assets/images/mars-elevation.png"

WIDTH = 4096
HEIGHT = 2048

os.makedirs("assets/images", exist_ok=True)

print("Loading MOLA elevation data...")

with rasterio.open(INPUT) as src:
    data = src.read(
        1,
        out_shape=(HEIGHT, WIDTH),
        masked=True,
        resampling=Resampling.bilinear
    )

elevation = data.astype(np.float32).filled(np.nan)
valid = np.isfinite(elevation)

if not valid.any():
    raise ValueError("No valid elevation pixels found.")

low, high = np.nanpercentile(elevation, [2, 98])

normalized = np.clip(
    (elevation - low) / (high - low),
    0, 1
)

colors = np.array([
    [18, 35, 80],
    [45, 85, 135],
    [105, 110, 120],
    [165, 105, 75],
    [210, 155, 105],
    [245, 215, 165]
], dtype=np.float32)

positions = np.linspace(0, 1, len(colors))

rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

for channel in range(3):
    rgb[:, :, channel] = np.interp(
        normalized,
        positions,
        colors[:, channel]
    ).astype(np.uint8)

rgb[~valid] = [12, 18, 30]

Image.fromarray(rgb, mode="RGB").save(OUTPUT)

print("Mars elevation texture generated!")
print("Output:", OUTPUT)
print("Dimensions:", WIDTH, "x", HEIGHT)
print("Elevation range:", low, "to", high)
heightmap = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

heightmap[valid] = (
    normalized[valid] * 255
).astype(np.uint8)

Image.fromarray(heightmap, mode="L").save(
    "assets/images/mars-height.png"
)

print("Heightmap generated!")