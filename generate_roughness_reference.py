
import os
import rasterio
import numpy as np
from rasterio.warp import transform_bounds, reproject
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from PIL import Image

SOURCE = "data/nasa/mola-roughness/mola_roughness.tif"
CTX = "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif"
OUTPUT = "assets/images/east-melas-roughness-reference.png"

WIDTH = 1024
HEIGHT = 1024

os.makedirs("assets/images", exist_ok=True)

print("Opening East Melas boundaries...")

with rasterio.open(CTX) as ctx:
    bounds = transform_bounds(
        ctx.crs,
        rasterio.open(SOURCE).crs,
        *ctx.bounds,
        densify_pts=21
    )

print("Regional bounds:", bounds)
print("Reading global MOLA reference map...")

with rasterio.open(SOURCE) as src:
    destination = np.zeros((3, HEIGHT, WIDTH), dtype=np.uint8)

    destination_transform = from_bounds(
        *bounds, WIDTH, HEIGHT
    )

    for band in range(1, 4):
        reproject(
            source=rasterio.band(src, band),
            destination=destination[band - 1],
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=destination_transform,
            dst_crs=src.crs,
            resampling=Resampling.bilinear
        )

image = np.moveaxis(destination, 0, -1)
Image.fromarray(image, mode="RGB").save(OUTPUT)

print("Reference image generated successfully.")
print("Output:", OUTPUT)
print("Dimensions:", WIDTH, "x", HEIGHT)
