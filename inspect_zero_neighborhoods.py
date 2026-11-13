
import rasterio
import numpy as np

dem_path = "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif"

# Zero locations found in your previous analysis
locations = [
    (1546, 3823),
    (1547, 3823),
    (1548, 3825),
    (1550, 3826),
    (1550, 3845),
    (1551, 3845)
]

with rasterio.open(dem_path) as dem:

    data = dem.read(1)

    print("ZERO PIXEL NEIGHBORHOOD ANALYSIS")
    print("--------------------------------")

    for row, col in locations:

        print(f"\nPixel at row {row}, column {col}")

        r1 = max(0, row - 3)
        r2 = min(dem.height, row + 4)
        c1 = max(0, col - 3)
        c2 = min(dem.width, col + 4)

        neighborhood = data[r1:r2, c1:c2]

        print(neighborhood)

        surrounding = neighborhood.copy()

        center_r = row - r1
        center_c = col - c1

        surrounding[center_r, center_c] = np.nan

        surrounding = surrounding.astype("float64")

        valid = surrounding[np.isfinite(surrounding)]

        print("Surrounding minimum:", np.min(valid))
        print("Surrounding maximum:", np.max(valid))
        print("Surrounding median:", np.median(valid))

print("\nNeighborhood analysis completed.")
