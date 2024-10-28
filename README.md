Scripts for Data Assimilation for the MER project.

This is the Data Assimilation part of the MER prototype.
It is executed after the preproc phase, and before the model and postproc phase of the MER chain. 
DA operates following these steps:
1. prepare the 3dvar directory by linking/preparing the needed input files (we expect that the preproc phase provides BGC ICs in netcdf format);
2. launch 3dvar;
3. take the 3dvar .nc output and generate new BGC ICs .dat for MIT (overwriting the previous ICs).

Before running main.sh, complete the *setup.sh and *.txt files. 
