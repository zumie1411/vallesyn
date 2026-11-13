
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt

from rasterio.enums import Resampling

INPUT = "data/processed/east_melas_slope.tif"

OUTPUT = "data/processed/east_melas_slope_visualization.png"

print("Opening existing slope GeoTIFF...")

if not os.path.exists(INPUT):
    raise FileNotFoundError(INPUT)

with rasterio.open(INPUT) as src:

    out_height = 1200
    out_width = int(
        src.width * out_height / src.height
    )

    # Read as a 2D array
    data = src.read(
        1,
        out_shape=(out_height, out_width),
        masked=True,
        resampling=Resampling.average
    )

    values = data.compressed()

    if values.size == 0:
        raise ValueError("No valid slope values found.")

    print("\nSLOPE STATISTICS")

    print("Minimum:", float(values.min()))
    print("Maximum:", float(values.max()))
    print("Mean:", float(values.mean()))
    print("Median:", float(np.median(values)))

    vmin, vmax = np.percentile(
        values, [2, 98]
    )

    plt.figure(figsize=(12, 10))

    image = plt.imshow(
        data,
        cmap="terrain",
        vmin=vmin,
        vmax=vmax,
        origin="upper"
    )

    plt.colorbar(
        image,
        label="Slope (degrees)"
    )

    plt.title(
        "Vallesyn - East Melas Terrain Slope Map"
    )

    plt.xlabel("West to East")
    plt.ylabel("North to South")

    plt.tight_layout()

    plt.savefig(
        OUTPUT,
        dpi=200,
        bbox_inches="tight"
    )

    plt.show()

print("\nVisualization successfully generated!")
print("Saved at:", OUTPUT)
