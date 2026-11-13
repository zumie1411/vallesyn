
import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling

dem_path = "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif"
ortho_path = "data/nasa/ctx-orthophoto/CTX_Ortho_12S290E_6mp_D18_034250_1676.tif"

with rasterio.open(dem_path) as dem, rasterio.open(ortho_path) as ortho:

    dem_data = dem.read(1)

    # Identify zero-valued DEM pixels
    dem_zero = dem_data == 0

    # Identify valid orthophoto pixels
    ortho_mask = (ortho.read_masks(1) > 0).astype("uint8")

    # Project orthophoto coverage onto the DEM grid
    ortho_on_dem = np.zeros(
        (dem.height, dem.width),
        dtype="uint8"
    )

    reproject(
        source=ortho_mask,
        destination=ortho_on_dem,
        src_transform=ortho.transform,
        src_crs=ortho.crs,
        dst_transform=dem.transform,
        dst_crs=dem.crs,
        resampling=Resampling.nearest
    )

    covered = ortho_on_dem == 1

    print("DEM total pixels:", dem_zero.size)
    print("DEM zero pixels:", np.count_nonzero(dem_zero))
    print("Orthophoto coverage on DEM grid:", np.count_nonzero(covered))

    print(
        "DEM zeros inside orthophoto coverage:",
        np.count_nonzero(dem_zero & covered)
    )

    print(
        "DEM zeros outside orthophoto coverage:",
        np.count_nonzero(dem_zero & ~covered)
    )

print("\nOrthophoto comparison completed.")
