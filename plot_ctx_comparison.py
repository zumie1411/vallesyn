
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.enums import Resampling

files = {
    "CTX DEM": "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif",
    "CTX Hillshade": "data/nasa/ctx-hillshade/CTX_Shade_East_Melas.tif"
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for row, (name, path) in enumerate(files.items()):

    with rasterio.open(path) as src:

        data = src.read(
            1,
            out_shape=(600, 1200),
            resampling=Resampling.nearest
        )

    zeros = data == 0

    # Original raster
    axes[row, 0].imshow(data, cmap="gray")
    axes[row, 0].set_title(name + " - Original")
    axes[row, 0].axis("off")

    # Zero-value mask
    axes[row, 1].imshow(zeros, cmap="gray", vmin=0, vmax=1)
    axes[row, 1].set_title(name + " - Zero-value locations")
    axes[row, 1].axis("off")

plt.tight_layout()

output = "data/processed/ctx_zero_comparison.png"
plt.savefig(output, dpi=150, bbox_inches="tight")

print("Comparison saved to:", output)

plt.show()
