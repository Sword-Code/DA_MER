
class Settings:
    dir_3dvar="/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/MER_3dvar/wrkdir/"
    DAtime_file='current_DA_time.txt'
    maskfile='/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/MER_3dvar/temp/mask.nc'
    varlistfile='DAvars.txt'
    
    def __init__(self):
        with open(DAtime_file, 'r') as f:
            line=f.readline()
        month=line[2:4]
        date=line[:8]
        datetime=line[:17]
