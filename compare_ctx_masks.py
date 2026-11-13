
import rasterio
import numpy as np

dem_path = "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif"
shade_path = "data/nasa/ctx-hillshade/CTX_Shade_East_Melas.tif"

with rasterio.open(dem_path) as dem, \
     rasterio.open(shade_path) as shade:

    if (dem.width, dem.height, dem.transform) != (
        shade.width, shade.height, shade.transform
    ):
        raise ValueError("The two rasters do not share the same grid.")

    dem_data = dem.read(1)
    shade_data = shade.read(1)

    dem_zero = dem_data == 0
    shade_zero = shade_data == 0

    agreement = np.mean(dem_zero == shade_zero) * 100

    print("DEM zero pixels:", np.count_nonzero(dem_zero))
    print("Hillshade zero pixels:", np.count_nonzero(shade_zero))
    print("Matching zero/non-zero classifications:",
          round(agreement, 4), "%")

    print("Both zero:", np.count_nonzero(dem_zero & shade_zero))
    print("DEM zero only:", np.count_nonzero(dem_zero & ~shade_zero))
    print("Hillshade zero only:",
          np.count_nonzero(~dem_zero & shade_zero))

print("\nComparison completed.")
