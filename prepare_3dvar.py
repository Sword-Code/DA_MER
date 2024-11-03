
# 1. symbolic link to BGC .nc files and EOFS
# 2. prepare sat file
# 3. compute misfits


import create_misfit
# import satellite
import sym_link

#1
sym_link.main()

#2
# satellite.main()

#3
create_misfit.main() 



