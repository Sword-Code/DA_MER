
. 3dvar2ICs_setup.sh

mpiexec python IC_files_gen_parallel.py --inputdir $inputdir --outmaskfile $maskfile --outputdir $outputdir --nativemask $maskfile --modelvarlist $varlistfile --time $DAtime
 
# should it be in a separated job? Take care to check how many task per node can run simultaniously in order to avoid RAM overflow.
