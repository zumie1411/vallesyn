
import rasterio

FILES = {
    "CTX DEM": "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif",
    "CTX Hillshade": "data/nasa/ctx-hillshade/CTX_Shade_East_Melas.tif"
}

for name, path in FILES.items():

    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    with rasterio.open(path) as src:

        print("\nDataset tags:")
        print(src.tags())

        print("\nImage structure:")
        print(src.tags(ns="IMAGE_STRUCTURE"))

        print("\nBand descriptions:")
        print(src.descriptions)

        print("\nBand 1 tags:")
        print(src.tags(1))

        print("\nMask flags:")
        print(src.mask_flag_enums)

        print("\nColor interpretation:")
        print(src.colorinterp)

        print("\nFiles:")
        print(src.files)

print("\nMetadata inspection completed.")
