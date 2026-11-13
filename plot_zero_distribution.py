
import rasterio
import numpy as np
import matplotlib.pyplot as plt
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

    row_edges = np.linspace(row_min, row_max + 1, 11).astype(int)
    col_edges = np.linspace(col_min, col_max + 1, 11).astype(int)

    counts = np.zeros((10, 10), dtype=int)

    for r in range(10):
        for c in range(10):
            region = zero_inside[
                row_edges[r]:row_edges[r+1],
                col_edges[c]:col_edges[c+1]
            ]
            counts[r, c] = np.count_nonzero(region)

    plt.figure(figsize=(10, 8))

    plt.imshow(counts, cmap="inferno", interpolation="nearest")
    plt.colorbar(label="Number of zero pixels")

    plt.title("CTX DEM Zero Pixels Inside Orthophoto Coverage")
    plt.xlabel("Grid Column")
    plt.ylabel("Grid Row")

    plt.xticks(range(10), range(1, 11))
    plt.yticks(range(10), range(1, 11))

    for r in range(10):
        for c in range(10):
            plt.text(c, r, str(counts[r, c]),
                     ha="center", va="center", color="white",
                     fontsize=8)

    plt.tight_layout()
    plt.savefig(
        "data/processed/ctx_overlap_zero_heatmap.png",
        dpi=200
    )

    plt.show()

print("Heatmap saved successfully.")
