
# 1. symbolic link to BGC .nc files
# 2. prepare sat file
# 3. compute misfits
# 4. symbolic link to EOFs

from setup import Settings

import satellite

import create_misfit

#0 
# get 3dvar meshmask.nc and other static files (horizontal correlations)

#1
#ln -sf ...

#2
satellite.main()

#3
create_misfit.main() 

#4
#ln -sf ...



