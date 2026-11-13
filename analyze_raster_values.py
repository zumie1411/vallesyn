
from pathlib import Path
import rasterio
import numpy as np

DATA_FOLDER = Path("data/nasa")

FILES = {
    "CTX DEM": "ctx-dem/CTX_DEM_East_Melas.tif",
    "CTX Orthophoto": "ctx-orthophoto/CTX_Ortho_12S290E_6mp_D18_034250_1676.tif",
    "CTX Hillshade": "ctx-hillshade/CTX_Shade_East_Melas.tif",
    "CTX Color Slope": "ctx-slope/CTX_ClrSlope_8bit_12S290E_24mp_D18_034250_1676_D21_035450_1674.tif",
    "MOLA Global DEM": "mola-global-dem/mola128_mola64_merge_90Nto90S_SimpleC_clon0.tif",
    "MOLA Roughness": "mola-roughness/mola_roughness.tif"
}

REPORT = DATA_FOLDER / "raster_value_analysis.txt"


def analyze_file(name, relative_path):
    path = DATA_FOLDER / relative_path

    print(f"\nAnalyzing: {name}")

    with rasterio.open(path) as src:
        # Read a reduced-size sample rather than the full raster.
        sample_width = min(1024, src.width)
        sample_height = min(1024, src.height)

        samples = src.read(
            out_shape=(src.count, sample_height, sample_width),
            masked=True,
            resampling=rasterio.enums.Resampling.nearest
        )

        lines = [
            f"DATASET: {name}",
            f"File: {path.name}",
            f"Dimensions: {src.width} x {src.height}",
            f"Sample size: {sample_width} x {sample_height}",
            f"Band count: {src.count}"
        ]

        for band_number in range(src.count):
            band = samples[band_number]
            values = band.compressed()

            lines.append(f"\nBand {band_number + 1}")

            if values.size == 0:
                lines.append("No valid sample values found.")
                continue

            lines.append(f"Valid sampled pixels: {values.size}")
            lines.append(f"Minimum: {float(np.min(values))}")
            lines.append(f"Maximum: {float(np.max(values))}")
            lines.append(f"Mean: {float(np.mean(values))}")
            lines.append(f"Median: {float(np.median(values))}")
            lines.append(f"Standard deviation: {float(np.std(values))}")

        return "\n".join(lines)


def main():
    reports = []

    for name, relative_path in FILES.items():
        try:
            result = analyze_file(name, relative_path)
            reports.append(result)
            print("Analysis successful.")

        except Exception as error:
            message = f"{name}: ERROR - {error}"
            reports.append(message)
            print(message)

    REPORT.write_text(
        "\n\n" + ("=" * 65) + "\n\n".join(reports),
        encoding="utf-8"
    )

    print("\n" + "=" * 50)
    print("PIXEL VALUE ANALYSIS COMPLETED")
    print(f"Report saved to: {REPORT}")
    print("=" * 50)


if __name__ == "__main__":
    main()
