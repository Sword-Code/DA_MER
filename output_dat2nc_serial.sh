
. output_dat2nc_setup.sh

python netcdf_convert.py --outputdir $outputdir --inputdir $inputdir --timelist $timelist --timestep $timestep --maskfile $maskfile --varlist $varlistfile --freq $freq
