
import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling

dem_path = "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif"
ortho_path = "data/nasa/ctx-orthophoto/CTX_Ortho_12S290E_6mp_D18_034250_1676.tif"

locations = [
    (1546, 3823),
    (1547, 3823),
    (1548, 3825),
    (1550, 3826),
    (1550, 3845),
    (1551, 3845)
]

with rasterio.open(dem_path) as dem, rasterio.open(ortho_path) as ortho:

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

    print("ORTHOPHOTO COVERAGE AT ZERO LOCATIONS")
    print("-------------------------------------")

    for row, col in locations:

        coverage = ortho_on_dem[row, col]

        print(
            f"Row {row}, Column {col}: "
            f"{'Valid orthophoto coverage' if coverage == 1 else 'No orthophoto coverage'}"
        )

print("\nComparison completed.")
