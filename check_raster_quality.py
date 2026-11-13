
from pathlib import Path
import rasterio
import numpy as np
from rasterio.transform import xy
from affine import Affine

DATA = Path("data/nasa")


FILES = {
    "CTX DEM": "ctx-dem/CTX_DEM_East_Melas.tif",

    "CTX Hillshade": "ctx-hillshade/CTX_Shade_East_Melas.tif",

    "CTX Orthophoto": "ctx-orthophoto/CTX_Ortho_12S290E_6mp_D18_034250_1676.tif",

    "MOLA Global DEM": "mola-global-dem/mola128_mola64_merge_90Nto90S_SimpleC_clon0.tif",

    "MOLA Roughness": "mola-roughness/mola_roughness.tif"
}


REPORT = DATA / "raster_quality_report.txt"


def inspect(name, relative_path):
    path = DATA / relative_path
    lines = [f"\n{'=' * 65}", name, f"File: {path.name}"]

    with rasterio.open(path) as src:
        # Preserve the original raster aspect ratio.
        scale = min(1200 / src.width, 1200 / src.height, 1)

        width = max(1, int(src.width * scale))
        height = max(1, int(src.height * scale))

        sample = src.read(
            out_shape=(src.count, height, width),
            masked=True,
            resampling=rasterio.enums.Resampling.nearest
        )

        sample_transform = src.transform * Affine.scale(
            src.width / width,
            src.height / height
        )

        lines.append(f"Original dimensions: {src.width} x {src.height}")
        lines.append(f"Sample dimensions: {width} x {height}")
        lines.append(f"Declared NoData: {src.nodata}")

        for index in range(src.count):
            band = sample[index]
            values = band.compressed()

            lines.append(f"\nBand {index + 1}")

            if values.size == 0:
                lines.append("No valid values found.")
                continue

            percentiles = np.percentile(
                values, [1, 5, 25, 50, 75, 95, 99]
            )

            lines.append(f"Valid sampled pixels: {values.size}")
            lines.append(f"Zero percentage: {np.mean(values == 0) * 100:.2f}%")
            lines.append(f"Minimum: {values.min()}")
            lines.append(f"Maximum: {values.max()}")

            lines.append(
                "Percentiles (1, 5, 25, 50, 75, 95, 99): "
                + str(percentiles)
            )

            
            raw = band.astype("float64").filled(np.nan)
            min_row, min_col = np.unravel_index(
                np.nanargmin(raw), raw.shape
            )
            max_row, max_col = np.unravel_index(
                np.nanargmax(raw), raw.shape
            )

            min_x, min_y = xy(
                sample_transform, min_row, min_col
            )
            max_x, max_y = xy(
                sample_transform, max_row, max_col
            )

            lines.append(
                f"Minimum location (projected): {min_x}, {min_y}"
            )
            lines.append(
                f"Maximum location (projected): {max_x}, {max_y}"
            )

    return "\n".join(lines)


def main():
    reports = []

    for name, filename in FILES.items():
        print(f"Checking {name}...")

        try:
            reports.append(inspect(name, filename))
            print("Completed.")
        except Exception as error:
            reports.append(f"{name}: ERROR: {error}")
            print(f"Error: {error}")

    REPORT.write_text("\n".join(reports), encoding="utf-8")

    print("\nQUALITY CHECK COMPLETED")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
