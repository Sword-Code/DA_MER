
### This is the Data Assimilation part of the MER prototype.
### It is executed after the preproc phase, and before the model and postproc phase of the MER chain. 
### DA operates following these steps:
### 1. prepare the 3dvar directory by linking/preparing the needed input files (we expect that the preproc phase provides BGC ICs in netcdf format);
### 2. launch 3dvar;
### 3. take the 3dvar .nc output and generate new BGC ICs .dat for MIT (overwriting the previous ICs).

PARALLEL=serial
# PARALLEL=parallel

### step 0
# activate python env + modules if necessary

### step 1
bash prepare_3dvar.sh

### step 2
bash run_3dvar.sh

### step 3
bash 3dvar2ICs_$PARALLEL.sh


