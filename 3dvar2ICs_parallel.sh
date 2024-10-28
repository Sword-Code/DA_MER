
. 3dvar2ICs_setup.sh

mpiexec python IC_files_gen.py --inputdir $inputdir --outmaskfile $maskfile --outputdir $outputdir --nativemask $maskfile --modelvarlist $varlistfile --time $timelist
 
# should it be in a separated job? Take care to check how many task per node can run simultaniously in order to avoid RAM overflow.
