
import setup
import os

class Settings(setup.Settings):
    eof_dst=os.path.join(setup.Settings.dir_3dvar,"eofs_chl.nc")
    IC_src="/leonardo_work/OGS23_PRACE_IT_0/sspada00/3dvar_MER_T1/TEMP/IC_test/{}.nc"
    IC_dst=os.path.join(setup.Settings.dir_3dvar,"DA__FREQ_1/RSTbefore.20150101-000000.{}.nc")
    
    def __init__(self):
        super().__init__()
        self.eof_src=os.path.join(self.dir_3dvar,f'static_data/EOF/eof.{self.month}.nc')
