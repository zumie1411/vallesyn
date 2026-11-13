
import rasterio
import numpy as np
from rasterio.enums import Resampling

FILES = {
    "CTX DEM": "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif",
    "CTX Hillshade": "data/nasa/ctx-hillshade/CTX_Shade_East_Melas.tif"
}

for name, path in FILES.items():
    print("\n------------------------------")
    print(name)
    print("------------------------------")

    with rasterio.open(path) as src:
        print("CRS:", src.crs)
        print("NoData:", src.nodata)
        print("Bounds:", src.bounds)

        # Read a smaller sample for inspection
        data = src.read(
            1,
            out_shape=(600, 1200),
            resampling=Resampling.nearest,
            masked=True
        )

        values = data.compressed()

        if values.size == 0:
            print("No valid pixels found!")
            continue

        zero_count = np.count_nonzero(values == 0)
        zero_percent = zero_count / values.size * 100

        print("Valid pixels:", values.size)
        print("Zero-valued pixels:", zero_count)
        print("Zero percentage:", round(zero_percent, 2), "%")
        print("Masked pixels:", np.ma.count_masked(data))

print("\nCTX coverage inspection completed.")
