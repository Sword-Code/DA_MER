
### 1. previous output .nc ->  prepare 3dvar directory
### 2. 3dvar
### 3pre. (optional) link 3dvar output to input_folder
### 3. generate ICs .dat (currently in MIT chain preproc: IC_files_gen.py)
### 4. run MIT
### 5. MIT output .dat -> .nc (already in MIT chain postproc: netcdf_convert.py)

PARALLEL=serial
# PARALLEL=parallel

### 0
# launch MIT chain preproc
# and activate python env + modules if necessary

. setup.sh

### 1
bash prepare_3dvar.sh

### 2
cd $dir_3dvar
bash launcher.sh   ### or run the job

### 3
bash 3dvar2ICs_$PARALLEL.sh

### 4
# MIT chain model step

### 5
# MIT chain postproc step

