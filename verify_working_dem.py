
import rasterio
import numpy as np

path = "data/processed/CTX_DEM_East_Melas_working_masked.tif"

with rasterio.open(path) as src:

    print("WORKING DEM VERIFICATION")
    print("------------------------")

    print("Dimensions:", src.width, "x", src.height)
    print("CRS:", src.crs)
    print("Resolution:", src.res)
    print("NoData:", src.nodata)
    print("Data type:", src.dtypes)

    data = src.read(1, masked=True)

    valid = data.compressed()

    print("\nPIXEL STATISTICS")
    print("Valid pixels:", len(valid))
    print("Masked pixels:", np.ma.count_masked(data))

    if len(valid) > 0:
        print("Minimum elevation:", valid.min())
        print("Maximum elevation:", valid.max())
        print("Mean elevation:", valid.mean())
        print("Median elevation:", np.median(valid))

print("\nVerification completed.")
