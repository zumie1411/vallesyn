
import rasterio
import numpy as np

source = "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif"

output = "data/processed/CTX_DEM_East_Melas_working_masked.tif"

NODATA = -9999.0

with rasterio.open(source) as src:

    profile = src.profile.copy()

    profile.update(
    dtype="float32",
    nodata=NODATA,
    compress="deflate",
    predictor=3,
    tiled=True,
    blockxsize=256,
    blockysize=256
)

    total_pixels = 0
    zero_pixels = 0

    with rasterio.open(output, "w", **profile) as dst:

       for _, window in src.block_windows(1):

            data = src.read(1, window=window).astype("float32")

            zero_mask = data == 0

            zero_pixels += np.count_nonzero(zero_mask)
            total_pixels += data.size

            data[zero_mask] = NODATA

            dst.write(data, 1, window=window)

print("Working DEM created.")
print("Total pixels:", total_pixels)
print("Zero pixels masked:", zero_pixels)
print("NoData value:", NODATA)
print("Output:", output)
