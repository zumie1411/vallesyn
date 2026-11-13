
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pathlib import Path

source = Path("data/processed/east_melas_slope.tif")
output = Path("data/processed/east_melas_slope_classes.tif")
image = Path("data/processed/east_melas_slope_classes.png")

print("Opening slope raster...")

with rasterio.open(source) as src:

    profile = src.profile.copy()
    profile.update(
        dtype="uint8",
        count=1,
        nodata=0,
        compress="deflate"
    )

    with rasterio.open(output, "w", **profile) as dst:

        for _, window in src.block_windows(1):

            data = src.read(1, window=window)
            valid = np.isfinite(data)

            if src.nodata is not None:
                valid &= data != src.nodata

            result = np.zeros(data.shape, dtype=np.uint8)

            result[valid & (data <= 5)] = 1
            result[valid & (data > 5) & (data <= 15)] = 2
            result[valid & (data > 15) & (data <= 30)] = 3
            result[valid & (data > 30) & (data <= 45)] = 4
            result[valid & (data > 45)] = 5

            dst.write(result, 1, window=window)

print("Slope classification completed!")

# Generate visualization
with rasterio.open(output) as src:

    data = src.read(
        1,
        out_shape=(1, min(1500, src.height),
                   min(1500, src.width))
    )

    data = np.ma.masked_equal(data, 0)

    cmap = ListedColormap([
        "green",
        "yellow",
        "orange",
        "red",
        "purple"
    ])

    plt.figure(figsize=(10, 9))

    plt.imshow(
        data,
        cmap=cmap,
        vmin=1,
        vmax=5,
        interpolation="nearest"
    )

    plt.title("Vallesyn - East Melas Slope Classification")
    plt.xlabel("West to East")
    plt.ylabel("North to South")

    cbar = plt.colorbar(ticks=[1, 2, 3, 4, 5])
    cbar.ax.set_yticklabels([
        "0-5 degrees",
        "5-15 degrees",
        "15-30 degrees",
        "30-45 degrees",
        "Above 45 degrees"
    ])

    plt.tight_layout()
    plt.savefig(image, dpi=200)
    plt.show()

print("Classification raster:", output)
print("Classification map:", image)
