
from pathlib import Path
import rasterio

# Main NASA data folder
DATA_FOLDER = Path("data/nasa")

# Inspection report destination
REPORT_FILE = DATA_FOLDER / "geotiff_inspection_report.txt"


def inspect_tiff(file_path):
    result = []

    result.append("=" * 70)
    result.append(f"FILE: {file_path.name}")
    result.append("=" * 70)

    # File size
    size_mb = file_path.stat().st_size / (1024 * 1024)
    result.append(f"File size: {size_mb:.2f} MB")

    # Open TIFF and inspect metadata only
    with rasterio.open(file_path) as src:

        result.append(f"Driver: {src.driver}")
        result.append(f"Width: {src.width} pixels")
        result.append(f"Height: {src.height} pixels")
        result.append(f"Bands: {src.count}")

        result.append(f"CRS: {src.crs}")
        result.append(
            f"Geographic CRS: "
            f"{src.crs.is_geographic if src.crs else 'Unknown'}"
        )

        result.append(f"Bounds: {src.bounds}")
        result.append(f"Resolution: {src.res}")
        result.append(f"Data types: {src.dtypes}")

        result.append(f"NoData values: {src.nodatavals}")
        result.append(f"Band units: {src.units}")
        result.append(f"Band descriptions: {src.descriptions}")

        result.append(f"Band scales: {src.scales}")
        result.append(f"Band offsets: {src.offsets}")
        result.append(f"Color interpretation: {src.colorinterp}")

        result.append("\nGENERAL METADATA:")
        result.append(str(src.tags()))

        result.append("\nIMAGE STRUCTURE:")
        result.append(str(src.tags(ns="IMAGE_STRUCTURE")))

    return "\n".join(result)


def main():

    # Find all TIFF files, including those in subfolders
    files = sorted(
        list(DATA_FOLDER.rglob("*.tif")) +
        list(DATA_FOLDER.rglob("*.tiff"))
    )

    if not files:
        print("No TIFF files found!")
        print("Check your data/nasa folder.")
        return

    print(f"Found {len(files)} TIFF files.")

    reports = []

    for number, file_path in enumerate(files, start=1):

        print(f"\nInspecting {number}/{len(files)}: {file_path.name}")

        try:
            report = inspect_tiff(file_path)
            reports.append(report)
            print("Successfully inspected!")

        except Exception as error:
            reports.append(
                f"ERROR: {file_path.name}\n{error}"
            )
            print(f"Inspection failed: {error}")

    # Save report
    REPORT_FILE.write_text(
        "\n\n".join(reports),
        encoding="utf-8"
    )

    print("\n" + "=" * 50)
    print("INSPECTION COMPLETED")
    print(f"Report saved at: {REPORT_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    main()
