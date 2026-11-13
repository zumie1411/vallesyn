
import rasterio
import numpy as np

path = "data/processed/mola_roughness_east_melas.tif"

with rasterio.open(path) as src:
    print("\n--- MOLA EAST MELAS EXTRACT ---")
    print("Dimensions:", src.width, "x", src.height)
    print("Number of bands:", src.count)
    print("CRS:", src.crs)
    print("Bounds:", src.bounds)
    print("Resolution:", src.res)
    print("NoData:", src.nodata)

    for band_number in range(1, src.count + 1):
        band = src.read(band_number, masked=True)
        values = band.compressed()

        print(f"\nBand {band_number}")

        if values.size == 0:
            print("No valid pixels found!")
            continue

        print("Valid pixels:", values.size)
        print("Minimum:", values.min())
        print("Maximum:", values.max())
        print("Mean:", round(float(values.mean()), 2))

print("\nInspection completed.")
