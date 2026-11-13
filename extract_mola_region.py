
import os
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

# Input NASA files
mola_path = "data/nasa/mola-roughness/mola_roughness.tif"
ctx_path = "data/nasa/ctx-dem/CTX_DEM_East_Melas.tif"

# Output file (the original will not be changed)
output_folder = "data/processed"
os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(
    output_folder,
    "mola_roughness_east_melas.tif"
)

print("Opening CTX DEM to identify the East Melas region...")

with rasterio.open(ctx_path) as ctx:
    ctx_bounds = ctx.bounds
    ctx_crs = ctx.crs

print("Opening MOLA Roughness...")

with rasterio.open(mola_path) as mola:

    # Convert the CTX DEM boundaries into MOLA's coordinate system
    bounds = transform_bounds(
        ctx_crs,
        mola.crs,
        *ctx_bounds,
        densify_pts=21
    )

    print("Regional boundaries:", bounds)

    # Find the matching section of the MOLA raster
    window = from_bounds(*bounds, transform=mola.transform)
    window = window.round_offsets().round_lengths()

    # Read the regional RGB data
    data = mola.read(window=window)

    # Prepare output metadata
    profile = mola.profile.copy()
    profile.update({
        "height": data.shape[1],
        "width": data.shape[2],
        "transform": mola.window_transform(window),
        "compress": "deflate"
    })

    # Save the regional extract
    with rasterio.open(output_path, "w", **profile) as output:
        output.write(data)

print("SUCCESS!")
print("Regional MOLA file saved at:", output_path)
