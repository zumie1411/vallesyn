
import rasterio

path = "data/processed/mola_roughness_east_melas.tif"

with rasterio.open(path) as src:

    print("=" * 55)
    print("MOLA ROUGHNESS METADATA INSPECTION")
    print("=" * 55)

    print("\nDataset metadata:")
    print(src.meta)

    print("\nDataset tags:")
    print(src.tags())

    print("\nBand information:")

    for band in range(1, src.count + 1):

        print(f"\nBAND {band}")
        print("Description:", src.descriptions[band - 1])
        print("Data type:", src.dtypes[band - 1])
        print("Color interpretation:", src.colorinterp[band - 1])
        print("Tags:", src.tags(band))

        data = src.read(band, masked=True)

        print("Minimum:", data.min())
        print("Maximum:", data.max())
        print("Mean:", data.mean())

    print("\nSubdatasets:", src.subdatasets)

    print("\nMetadata inspection completed.")
