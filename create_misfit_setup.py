import setup

class Settings(setup.Settings):
    IC_file="/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/MER_3dvar/temp/IC_test/P{}l.nc"
    misfit_file="/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/MER_3dvar/wrkdir/chl_mis.nc"

    sat_var='CHL'
    sat_lon_var='lon'
    sat_lat_var='lat'
    IC_var='P{}l'
    var_var='variance'

    max_std=0.73

    fillValue=1.0e+20
    time_val=1.
    depth_val=1.47210180759 
    
    def __init__(self):
        super().__init__()
        self.sat_file=f"/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/MER_3dvar/temp/1_24/{self.date}_cmems_obs-oc_med_bgc-plankton_myint_l3-multi-1km_P1D.nc"
        self.var_file=f'/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/MER_3dvar/temp/SAT_VAR/var2D.{self.month}.nc'
