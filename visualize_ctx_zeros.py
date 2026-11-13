
import rasterio
import numpy as np

FILES = {
    "CTX DEM": "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif",
    "CTX Hillshade": "data/nasa/ctx-hillshade/CTX_Shade_East_Melas.tif"
}

ROWS = 20
COLS = 40

for name, path in FILES.items():

    print("\n" + "=" * 45)
    print(name)
    print("=" * 45)

    with rasterio.open(path) as src:

        for r in range(ROWS):
            row_start = int(r * src.height / ROWS)
            row_end = int((r + 1) * src.height / ROWS)

            stripe = src.read(
                1,
                window=((row_start, row_end), (0, src.width))
            )

            line = ""

            for c in range(COLS):
                col_start = int(c * src.width / COLS)
                col_end = int((c + 1) * src.width / COLS)

                block = stripe[:, col_start:col_end]

                zero_fraction = np.count_nonzero(
                    block == 0
                ) / block.size

                if zero_fraction >= 0.75:
                    line += "#"
                elif zero_fraction >= 0.10:
                    line += "+"
                else:
                    line += "."

            print(line)

print("\nCorrected spatial inspection completed.")

