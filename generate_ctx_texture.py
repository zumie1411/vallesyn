
import os
import numpy as np
import rasterio
from rasterio.enums import Resampling
from PIL import Image

INPUT = "data/processed/CTX_DEM_East_Melas_working_masked.tif"
OUTPUT_DIR = "assets/images"

WIDTH = 1024
HEIGHT = 2650

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading East Melas CTX DEM...")

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
    raise ValueError("No valid CTX elevation pixels found.")

low, high = np.nanpercentile(elevation, [2, 98])

if high <= low:
    raise ValueError("Invalid elevation range.")

normalized = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

normalized[valid] = np.clip(
    (elevation[valid] - low) / (high - low),
    0,
    1
)

colors = np.array([
    [20, 28, 35],
    [65, 75, 75],
    [115, 105, 85],
    [165, 130, 95],
    [215, 180, 135],
    [245, 220, 180]
], dtype=np.float32)

positions = np.linspace(0, 1, len(colors))

rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

for channel in range(3):
    rgb[:, :, channel] = np.interp(
        normalized,
        positions,
        colors[:, channel]
    ).astype(np.uint8)

# Create RGBA texture.
# Valid terrain is opaque; NoData pixels are transparent.

rgba = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)

rgba[:, :, :3] = rgb
rgba[valid, 3] = 255

Image.fromarray(rgba, mode="RGBA").save(
    f"{OUTPUT_DIR}/east-melas-ctx.png"
)

# Generate elevation heightmap.

heightmap = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

heightmap[valid] = (
    normalized[valid] * 255
).astype(np.uint8)

Image.fromarray(heightmap, mode="L").save(
    f"{OUTPUT_DIR}/east-melas-height.png"
)

print()
print("East Melas textures generated successfully!")
print("Elevation range:", low, "to", high)
print("Dimensions:", WIDTH, "x", HEIGHT)
print("Valid pixels:", int(valid.sum()))
print("NoData pixels:", int((~valid).sum()))
print("Output: assets/images/east-melas-ctx.png")
print("Output: assets/images/east-melas-height.png")
