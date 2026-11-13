
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.enums import Resampling

path = "data/processed/CTX_DEM_East_Melas_working_masked.tif"

with rasterio.open(path) as src:

    data = src.read(
        1,
        out_shape=(1100, 425),
        masked=True,
        resampling=Resampling.nearest
    )

    data = np.ma.masked_invalid(data)

plt.figure(figsize=(12, 9))

cmap = plt.colormaps["terrain"].copy()
cmap.set_bad("black")

image = plt.imshow(data, cmap=cmap)

plt.colorbar(image, label="Elevation (provisional, metres)")
plt.title("Vallesyn - East Melas CTX Elevation Model")
plt.xlabel("West to East")
plt.ylabel("North to South")

plt.tight_layout()

plt.savefig(
    "data/processed/working_dem_visualization.png",
    dpi=200
)

plt.show()

print("Elevation visualization saved successfully.")
