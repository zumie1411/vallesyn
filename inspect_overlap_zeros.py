
import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling

dem_path = "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif"
ortho_path = "data/nasa/ctx-orthophoto/CTX_Ortho_12S290E_6mp_D18_034250_1676.tif"

with rasterio.open(dem_path) as dem, rasterio.open(ortho_path) as ortho:

    dem_data = dem.read(1)

    ortho_mask = (ortho.read_masks(1) > 0).astype("uint8")

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

    overlap = ortho_on_dem == 1
    zero_inside = (dem_data == 0) & overlap

    print("OVERLAP ZERO ANALYSIS")
    print("---------------------")

    print("Total overlap pixels:", np.count_nonzero(overlap))
    print("Zero pixels in overlap:", np.count_nonzero(zero_inside))

    rows, cols = np.where(zero_inside)

    print("\nFirst 20 zero pixel locations (row, column):")

    for row, col in zip(rows[:20], cols[:20]):
        print(row, col)

    if len(rows) > 0:
        print("\nBounding box of overlap zeros:")
        print("Minimum row:", rows.min())
        print("Maximum row:", rows.max())
        print("Minimum column:", cols.min())
        print("Maximum column:", cols.max())

print("\nAnalysis completed.")
