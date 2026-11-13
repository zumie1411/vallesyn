
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

    rows, cols = np.where(overlap)

    row_min, row_max = rows.min(), rows.max()
    col_min, col_max = cols.min(), cols.max()

    print("ZERO DISTRIBUTION BY GRID")
    print("-------------------------")

    row_edges = np.linspace(row_min, row_max + 1, 11).astype(int)
    col_edges = np.linspace(col_min, col_max + 1, 11).astype(int)

    results = []

    for r in range(10):
        for c in range(10):

            region = zero_inside[
                row_edges[r]:row_edges[r+1],
                col_edges[c]:col_edges[c+1]
            ]

            count = np.count_nonzero(region)

            if count > 0:
                results.append((count, r + 1, c + 1))

    results.sort(reverse=True)

    print("Top 10 grid sections containing zero pixels:")

    for count, r, c in results[:10]:
        print(f"Grid row {r}, column {c}: {count} zero pixels")

    print("\nTotal zero pixels:", np.count_nonzero(zero_inside))

print("\nDistribution analysis completed.")
