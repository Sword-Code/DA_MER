
. output_dat2nc_setup.sh

mpiexec python netcdf_convert.py --outputdir $outputdir --inputdir $inputdir --timelist $timelist --timestep $timestep --maskfile $maskfile --varlist $varlistfile --freq $freq

# should it be in a separated job? Take care to check how many task per node can run simultaniously in order to avoid RAM overflow.
 
