
class Settings:
    dir_3dvar="/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/MER_3dvar/wrkdir/"
    DAtime_file='current_DA_time.txt'
    maskfile='/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/TEMP/mask.nc'
    varlistfile='/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/MER_3dvar/DAvars.txt'
    
    def __init__(self):
        with open(self.DAtime_file, 'r') as f:
            line=f.readline()
        self.month=line[4:6]
        self.date=line[:8]
        self.datetime=line[:17]
        
        with open(self.varlistfile, 'r') as f:
            lines=f.readlines()
        lines=[line.strip() for line in lines]
        self.DAvars=[line for line in lines if line!=""]
