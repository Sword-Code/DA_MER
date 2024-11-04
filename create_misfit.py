 
import netCDF4 as nc
from scipy.io import netcdf_file
import os
import numpy as np

from create_misfit_setup import Settings

def misfit(settings):
    transpose=False
    
    print('reading sat file: '+settings.sat_file)
    with nc.Dataset(settings.sat_file, "r") as sat_nc:
        chl=sat_nc[settings.sat_var][:]
        sat_lon=sat_nc[settings.sat_lon_var][:]
        sat_lat=sat_nc[settings.sat_lat_var][:]
    chl=np.squeeze(chl)

    for i in range(1,5):
        filename=settings.IC_file.format(i)
        print('reading input file: '+filename)
        with nc.Dataset(filename, "r") as ic_nc:
            ic=ic_nc[settings.IC_var.format(i)][...,0,:,:]
        ic=np.squeeze(ic)
        chl-=ic

    print('reading variance file: '+settings.var_file)
    with nc.Dataset(settings.var_file,'r') as  var_nc:
        var=var_nc[settings.var_var][:]
    var=np.squeeze(var)
    std=np.sqrt(var)
    std[std>settings.max_std]=settings.max_std
    std.mask=np.logical_or(std.mask, chl.mask)
    std.data[std.mask]=settings.fillValue
    std.fill_value=settings.fillValue
    
    chl.mask=std.mask
    chl.data[chl.mask]=settings.fillValue
    chl.fill_value=settings.fillValue

    n_lat,n_lon=chl.shape

    print('writing misfit file: '+settings.misfit_file)
    # with nc.Dataset(settings.misfit_file, 'w) as mis_nc:
    with netcdf_file(settings.misfit_file, 'w') as mis_nc:
        mis_nc.createDimension("time", 1)
        mis_nc.createDimension("depth", 1)
        mis_nc.createDimension("lon", n_lon)
        mis_nc.createDimension("lat", n_lat)
        
        time=mis_nc.createVariable("time", np.float32, ("time",))
        depth=mis_nc.createVariable("depth", np.float32, ("depth",))
        lon=mis_nc.createVariable("lon", np.float32, ("lon",))
        lat=mis_nc.createVariable("lat", np.float32, ("lat",))
        if transpose:
            misfchl=mis_nc.createVariable("misfchl", np.float32, ("lon",'lat'))
            errchl=mis_nc.createVariable("errchl", np.float32, ("lon",'lat'))
        else:
            misfchl=mis_nc.createVariable("misfchl", np.float32, ("lat",'lon'))
            errchl=mis_nc.createVariable("errchl", np.float32, ("lat",'lon'))
            
        time._FillValue=settings.fillValue
        depth._FillValue=settings.fillValue
        lon._FillValue=settings.fillValue
        lat._FillValue=settings.fillValue
        errchl._FillValue=settings.fillValue
        misfchl._FillValue=settings.fillValue
        
        errchl.info='ERRsat read from file: '+settings.var_file
        misfchl.type='chl concentrations'
        
        lon[:]=sat_lon
        lat[:]=sat_lat
        depth[:]=settings.depth_val
        time[:]=settings.time_val
        if transpose:
            misfchl[:]=chl.transpose()
            errchl[:]=std.transpose()
        else:
            misfchl[:]=chl
            errchl[:]=std
            
    print('misfit done')
        
def main():
    settings=Settings()
    misfit(settings)

if __name__ == "__main__":
    main()
    

    
    
    
    
