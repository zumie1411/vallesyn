
import rasterio

files = {
    "DEM": "data/processed/CTX_DEM_East_Melas_working_masked.tif",
    "Slope": "data/processed/east_melas_slope.tif",
    "MOLA Roughness": "data/processed/mola_roughness_east_melas.tif"
}

datasets = {}

for name, path in files.items():
    print("\n" + "=" * 50)
    print(name)

    with rasterio.open(path) as src:
        datasets[name] = {
            "shape": src.shape,
            "crs": src.crs,
            "transform": src.transform,
            "bounds": src.bounds,
            "resolution": src.res,
            "count": src.count,
            "dtype": src.dtypes
        }

        print("Dimensions:", src.shape)
        print("CRS:", src.crs)
        print("Resolution:", src.res)
        print("Bounds:", src.bounds)
        print("Transform:", src.transform)
        print("Bands:", src.count)
        print("Data types:", src.dtypes)
        print("Color interpretation:", src.colorinterp)

dem = datasets["DEM"]
slope = datasets["Slope"]

print("\n" + "=" * 50)
print("DEM AND SLOPE ALIGNMENT")

print("Same dimensions:", dem["shape"] == slope["shape"])
print("Same CRS:", dem["crs"] == slope["crs"])
print("Same transform:", dem["transform"] == slope["transform"])
print("Same bounds:", dem["bounds"] == slope["bounds"])

if (
    dem["shape"] == slope["shape"]
    and dem["crs"] == slope["crs"]
    and dem["transform"] == slope["transform"]
):
    print("\nSUCCESS: DEM and Slope are spatially aligned.")
else:
    print("\nWARNING: Alignment correction is required.")

print("\nMOLA ROUGHNESS INFORMATION")
print("Bands:", datasets["MOLA Roughness"]["count"])
print("Resolution:", datasets["MOLA Roughness"]["resolution"])

print("\nInspection completed.")
