
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt

from rasterio.windows import Window
from rasterio.enums import Resampling

# ==========================================
# VALLESYN - EAST MELAS TERRAIN SLOPE
# ==========================================

INPUT_DEM = (
    "data/processed/"
    "CTX_DEM_East_Melas_working_masked.tif"
)

OUTPUT_DIR = "data/processed"

OUTPUT_SLOPE = os.path.join(
    OUTPUT_DIR,
    "east_melas_slope.tif"
)

OUTPUT_IMAGE = os.path.join(
    OUTPUT_DIR,
    "east_melas_slope_visualization.png"
)

NODATA = -9999.0
BLOCK_SIZE = 256

os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():

    print("=" * 55)
    print("VALLESYN - TERRAIN SLOPE ANALYSIS")
    print("=" * 55)

    if not os.path.exists(INPUT_DEM):
        raise FileNotFoundError(
            f"Working DEM not found: {INPUT_DEM}"
        )

    valid_pixel_count = 0

    with rasterio.open(INPUT_DEM) as src:

        print("\nOpening working DEM...")

        print("Dimensions:", src.width, "x", src.height)
        print("Resolution:", src.res)
        print("CRS:", src.crs)
        print("NoData:", src.nodata)

        # Horizontal pixel dimensions in metres
        xres = abs(src.transform.a)
        yres = abs(src.transform.e)

        if xres == 0 or yres == 0:
            raise ValueError("Invalid DEM resolution.")

        profile = src.profile.copy()

        profile.update(
            driver="GTiff",
            dtype="float32",
            count=1,
            nodata=NODATA,
            compress="deflate",
            predictor=3,
            tiled=True,
            blockxsize=256,
            blockysize=256
        )

        print("\nCreating slope GeoTIFF...")

        with rasterio.open(
            OUTPUT_SLOPE,
            "w",
            **profile
        ) as dst:

            # Process the large DEM in manageable blocks
            total_rows = src.height
            total_cols = src.width

            total_blocks = (
                ((total_rows + BLOCK_SIZE - 1) // BLOCK_SIZE)
                *
                ((total_cols + BLOCK_SIZE - 1) // BLOCK_SIZE)
            )

            completed_blocks = 0

            for row in range(0, total_rows, BLOCK_SIZE):

                for col in range(0, total_cols, BLOCK_SIZE):

                    height = min(
                        BLOCK_SIZE,
                        total_rows - row
                    )

                    width = min(
                        BLOCK_SIZE,
                        total_cols - col
                    )

                    # Add a one-pixel border around each block
                    # to avoid artificial slope discontinuities.

                    r0 = max(0, row - 1)
                    c0 = max(0, col - 1)

                    r1 = min(
                        total_rows,
                        row + height + 1
                    )

                    c1 = min(
                        total_cols,
                        col + width + 1
                    )

                    read_window = Window(
                        c0,
                        r0,
                        c1 - c0,
                        r1 - r0
                    )

                    masked = src.read(
                        1,
                        window=read_window,
                        masked=True
                    )

                    elevation = np.asarray(
                        masked.filled(np.nan),
                        dtype=np.float32
                    )

                    # Calculate elevation gradients
                    dz_dy, dz_dx = np.gradient(
                        elevation,
                        yres,
                        xres
                    )

                    # Calculate slope in radians
                    gradient = np.sqrt(
                        dz_dx ** 2 + dz_dy ** 2
                    )

                    # Convert radians into degrees
                    slope = np.degrees(
                        np.arctan(gradient)
                    )

                    # Extract the original block
                    r_start = row - r0
                    c_start = col - c0

                    slope_block = slope[
                        r_start:r_start + height,
                        c_start:c_start + width
                    ]

                    # Preserve invalid areas as NoData
                    valid = np.isfinite(slope_block)

                    output_block = np.full(
                        (height, width),
                        NODATA,
                        dtype=np.float32
                    )

                    output_block[valid] = (
                        slope_block[valid]
                    )

                    valid_pixel_count += int(
                        np.count_nonzero(valid)
                    )

                    dst.write(
                        output_block,
                        1,
                        window=Window(
                            col,
                            row,
                            width,
                            height
                        )
                    )

                    completed_blocks += 1

                    if completed_blocks % 50 == 0:
                        print(
                            f"Processed {completed_blocks}"
                            f"/{total_blocks} blocks"
                        )

    print("\nSlope calculation completed!")

    print("Valid slope pixels:", valid_pixel_count)

    print("Output:", OUTPUT_SLOPE)

    # ==========================================
    # GENERATE VISUALIZATION
    # ==========================================

    print("\nGenerating slope visualization...")

    with rasterio.open(OUTPUT_SLOPE) as src:

        out_height = 1200
        out_width = max(
            1,
            int(src.width * out_height / src.height)
        )

        data = src.read(
            1,
            out_shape=(1, out_height, out_width),
            masked=True,
            resampling=Resampling.average
        )

        values = data.compressed()

        if values.size == 0:
            raise ValueError("No valid slope values found.")

        # Percentile scaling improves visual contrast
        vmin, vmax = np.percentile(
            values,
            [2, 98]
        )

        plt.figure(figsize=(12, 10))

        image = plt.imshow(
            data[0],
            cmap="terrain",
            vmin=vmin,
            vmax=vmax,
            origin="upper"
        )

        plt.colorbar(
            image,
            label="Slope (degrees)"
        )

        plt.title(
            "Vallesyn - East Melas Terrain Slope Map"
        )

        plt.xlabel("West to East")
        plt.ylabel("North to South")

        plt.tight_layout()

        plt.savefig(
            OUTPUT_IMAGE,
            dpi=200,
            bbox_inches="tight"
        )

        plt.show()

    print("\n" + "=" * 55)
    print("VALLESYN SLOPE ANALYSIS COMPLETED")
    print("=" * 55)

    print("Slope GeoTIFF:", OUTPUT_SLOPE)
    print("Visualization:", OUTPUT_IMAGE)


if __name__ == "__main__":
    main()
