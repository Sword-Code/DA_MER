import os
import glob
import sys
import json
import netCDF4 as nc
import numpy as np
import numpy.ma as ma
from typing import Dict
#from alive_progress import alive_bar

import scipy.interpolate as intrp



def interpolate_3d(values2interp, old_lon, old_lat, old_dep, new_grid, namevar):
    """
    Interpolates 3D data (lat, lon, dep) from an old grid to a new grid using nearest neighbor interpolation.

    Args:
        values2interp: 3D array (lon, lat, dep) to be interpolated.
        old_lon: 1D array of old longitudes.
        old_lat: 1D array of old latitudes.
        old_dep: 1D array of old depths.
        new_grid: Dictionary containing 'longitude', 'latitude', and 'depth' arrays for the new grid.
        namevar: Variable name to extract from the new grid.

    Returns:
        Interpolated 3D array on the new grid.
    """
    # Get the new longitudes, latitudes, and depths
    new_lon = new_grid['longitude'][:]
    new_lat = new_grid['latitude'][:]
    new_dep = new_grid['depth'][:]

    # Create 3D meshgrid for old and new grids
    old_dep, old_lon, old_lat  = np.meshgrid(old_dep, old_lat, old_lon,  indexing='ij')
    new_dep, new_lon, new_lat = np.meshgrid(new_dep, new_lat, new_lon, indexing='ij')

    # Extract the data to be interpolated
    new_data = new_grid[namevar][:]
    print("shape", new_data.shape)

    # Apply mask if the data is masked (land points or invalid values)
    masked_data = np.ma.masked_invalid(values2interp)  # Mask invalid values (NaNs, etc.)
    new_mask = np.ma.masked_invalid(new_data)
    new_mask = new_mask.mask  # Extract the mask

    # Create a mask of valid (non-masked) points
    valid_mask = ~masked_data.mask

    # Apply the mask to both the coordinates and values
    points = np.vstack((old_lon[valid_mask], old_lat[valid_mask], old_dep[valid_mask])).T  # Only valid (lon, lat, dep) points
    values = masked_data[valid_mask]  # Only valid data values

    # Create new points on the target grid for interpolation
    grid_points = np.vstack((new_lon.ravel(), new_lat.ravel(), new_dep.ravel())).T

    # Perform nearest neighbor interpolation
    interp_data = intrp.griddata(points, values, grid_points, method='nearest')

    # Reshape back to the grid shape of the target
    interp_data = interp_data.reshape(new_lon.shape)
    interp_data = ma.masked_array(interp_data, mask=new_mask, fill_value=1e+20, dtype=np.float32)

    return interp_data


def interpolate_2d(values2interp, old_lon, old_lat, new_grid, namevar):
    """
    Interpolates 3D data (lat, lon, dep) from an old grid to a new grid using nearest neighbor interpolation.

    Args:
        values2interp: 2D array (lon, lat) to be interpolated.
        old_lon: 1D array of old longitudes.
        old_lat: 1D array of old latitudes.
        new_grid: Dataset containing 'longitude' and 'latitude' arrays for the new grid.
        namevar: Variable name to extract from the new grid.

    Returns:
        Interpolated 2D array on the new grid.
    """
    # Get the new longitudes and latitudes
    new_lon = new_grid['longitude'][:]
    new_lat = new_grid['latitude'][:]

    # Create 3D meshgrid for old and new grids
    old_lon, old_lat  = np.meshgrid(old_lat, old_lon,  indexing='ij')
    new_lon, new_lat = np.meshgrid(new_lat, new_lon, indexing='ij')

    # Extract the data to be interpolated (only surface)
    new_data = new_grid[namevar][0, :]

    # Apply mask if the data is masked (land points or invalid values)
    masked_data = np.ma.masked_invalid(values2interp)  # Mask invalid values (NaNs, etc.)
    new_mask = np.ma.masked_invalid(new_data)
    new_mask = new_mask.mask  # Extract the mask

    # Create a mask of valid (non-masked) points
    valid_mask = ~masked_data.mask
    print(valid_mask.shape)
    # Apply the mask to both the coordinates and values
    points = np.vstack((old_lon[valid_mask], old_lat[valid_mask])).T  # Only valid (lon, lat) points
    values = masked_data[valid_mask]  # Only valid data values

    # Create new points on the target grid for interpolation
    grid_points = np.vstack((new_lon.ravel(), new_lat.ravel())).T

    # Perform nearest neighbor interpolation
    interp_data = intrp.griddata(points, values, grid_points, method='nearest')

    # Reshape back to the grid shape of the target
    interp_data = interp_data.reshape(new_lon.shape)
    interp_data = ma.masked_array(interp_data, mask=new_mask, fill_value=1e+20, dtype=np.float32)

    return interp_data


def interpolate_data(cms_name: str, input_path: str, output_path: str, grid_file: str, var_grid, n_dim: int = 3) -> None:
    '''
        Performs the interpolation of a given variable and saves the results into a different folder.

        Args:
            cms_name (str): variable name.
            input_path (str): directory containing the input data data.
            output_path (str): directory to put the output file
            grid_file (str): the NetCDF file that contains the target grid for interpolation.
            var_grid (str): the variable in grid_file on lon and lat (to extract the mask)
            n_dim (optional): the number of spatial dimensions 
    '''

    source_dir = input_path
    destination_dir = output_path

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    # Open the grid file once for interpolation
    with nc.Dataset(grid_file, "r") as grid_nc:
        new_longitudes = grid_nc['lon'][:]
        new_latitudes = grid_nc['lat'][:]  # New latitude and longitude values
        if n_dim == 3:
            new_depth = grid_nc['dep'][:]

        # with alive_bar(0, title=f"Interpolating data...") as bar:
        if True:
            
            # Iterate over the NetCDF files in the source directory
            for file_path in glob.glob(os.path.join(source_dir, "*.nc")):
                # Open the original NetCDF file for reading
                with nc.Dataset(file_path, "r") as source_nc:
                    source_file_name = os.path.basename(file_path)
                    source_ds = nc.Dataset(file_path)

                    old_lon = source_ds['longitude'][:]
                    old_lat = source_ds['latitude'][:]
                    if n_dim == 3:
                        old_dep = source_ds['depth'][:]

                    old_data = source_ds[cms_name][:]
                    # Define the path for the modified version in the destination directory
                    new_file_path = os.path.join(destination_dir, source_file_name)

                    if not os.path.exists(new_file_path):
                    # Create a new NetCDF file for writing
                        with nc.Dataset(new_file_path, "w") as dest_nc:
                            # Create dimensions in the new file based on the interpolated grid
                            if n_dim == 3:
                                dest_nc.createDimension("depth", len(new_depth))
                            dest_nc.createDimension("longitude", len(new_longitudes))
                            dest_nc.createDimension("latitude", len(new_latitudes))

                            # Create depth, latitude, and longitude variables in the new file
                            if n_dim == 3:
                                dest_depth = dest_nc.createVariable("depth", new_depth.dtype, ("depth",))
                            dest_longitudes = dest_nc.createVariable("longitude", new_longitudes.dtype, ("longitude",))
                            dest_latitudes = dest_nc.createVariable("latitude", new_latitudes.dtype, ("latitude",))

                            # Write the new depth, latitude, and longitude values
                            if n_dim == 3:
                                dest_depth[:] = new_depth
                            dest_longitudes[:] = new_longitudes
                            dest_latitudes[:] = new_latitudes

                            # Perform interpolation
                            # Create a variable in the new file and write the interpolated array
                            if n_dim == 3:
                                interpolated_array = interpolate_3d(old_data, old_lon, old_lat, old_dep, grid_nc, cms_name)
                                spatial_dim = ("depth", "latitude", "longitude")
                            else:
                                #sat_data has time as 1st dim
                                interpolated_array = interpolate_2d(old_data[0, :], old_lon, old_lat, grid_nc, var_grid)
                                spatial_dim = ("latitude", "longitude")
                            dest_array = dest_nc.createVariable(cms_name, interpolated_array.dtype, spatial_dim)
                            dest_array[:] = interpolated_array
                            print(dest_array)

                            # Copy global attributes from the original file
                            dest_nc.setncatts(source_nc.__dict__)
                    else:
                        print(f"{new_file_path} have already been created")
                    # bar()






if __name__ == "__main__":
    '''
        Interpolate the files present in the source directory to match the dimensions with those of the files in the 
        target directory.
        The files should be in a directory with the name of the variable in the source directory

        Parameters:
        -ip path to the input dir
        -op path to the output dir
        -v variable to interpolate
    '''
    i = 1
    var = None
    input_path = None
    output_path = None

    while i < len(sys.argv):
        if sys.argv[i] == "-ip":
            if input_path is not None: raise ValueError("Repeated input for data path")
            input_path = sys.argv[i+1]
            i += 2      
        elif sys.argv[i] == "-op":
            if output_path is not None: raise ValueError("Repeated input for data path")
            output_path = sys.argv[i+1]
            i += 2   
        elif sys.argv[i] == "-v":
            if var is not None : raise ValueError("Repeated input for variable")
            var = sys.argv[i+1]
            i += 2
        else:
            i += 1

    if input_path is None: raise TypeError("Missing value for input path")
    if output_path is None: raise TypeError("Missing value for output path")


    if var == None: raise TypeError("Missing value for variable")


    # Path to the file containing the grid to be used for interpolation
    grid_file_path = os.path.join("/data/initial_data/NARF_nc/Chla/Chla_2006_054.nc")


    print(f"[interpolate for variable '{var}'] Starting execution")
    print(os.path.join(input_path, var))
    interpolate_data(var, os.path.join(input_path, var), os.path.join(output_path, var), grid_file_path, "Chla", n_dim=2)
    print(f"[interpolate for variable '{var}'] Ending execution")

