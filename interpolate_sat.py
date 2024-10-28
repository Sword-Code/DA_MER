 
import argparse
import os

import numpy as np
import scipy.io as NC
from bitsea.commons import netcdf4
from bitsea.commons.dataextractor import DataExtractor
from bitsea.commons.mask import Mask
from bitsea.commons.utils import addsep
from bitsea.commons.utils import file2stringlist

from .general import mask
from .general import NetCDF_phys_Files
from .general import NetCDF_phys_Vars
from .general import space_intepolator_griddata


def argument():
    parser = argparse.ArgumentParser(
        description=(
            "Interpolates sat observation in the domain defined by outmaskfile."
        )
    )
    parser.add_argument(
        "--inputdir", "-i", type=str, required=True, help="/some/path/"
    )
    parser.add_argument(
        "--outmaskfile",
        "-m",
        type=str,
        required=True,
        help="/some/path/outmask.nc",
    )
    parser.add_argument(
        "--outputdir", "-o", type=str, required=True, help="/some/path/"
    )
    parser.add_argument(
        "--nativemask",
        type=str,
        required=True,
        help="NetCDF File name of the mask on which inputs are defined.",
    )
    parser.add_argument(
        "--satvar",
        "-v",
        type=str,
        default=None,
        help="name of the variable, ex.: CHL",
    )
    parser.add_argument(
        "--suffix",
        "-s",
        type=str,
        default=None,
        help="satellite suffix string",
    )
    parser.add_argument(
        "--timelist",
        "-t",
        type=str,
        required=True,
        help="/some/path/filename. A file with satellite dates.",
    )

    return parser.parse_args()

try:
    from mpi4py import MPI
    comm  = MPI.COMM_WORLD
    rank  = comm.Get_rank()
    nranks =comm.size
    isParallel = True
except:
    rank   = 0
    nranks = 1
    isParallel = False


def writeSatFile(*, M, outputfile, var, Mask1, Mask2):
    Mcheck = M.copy()

    NCout = NC.netcdf_file(outputfile, "w")
    NCout.createDimension("Lon", Mask2.Lon.size)
    NCout.createDimension("Lat", Mask2.Lat.size)
    
    ##### should it be fixed? how sat mask is done?
    NCout.createDimension("Depth", Mask2.jpk)
    ncvar = NCout.createVariable(var, "f", ("Depth", "Lat", "Lon"))
    #####
    
    setattr(ncvar, "missing_value", 1.0e20)
    ncvar[:] = Mcheck
    NCout.close()


def gen_sat_files(
    *, inputdir, outputdir, nativemask, timelist, outmaskfile, satvar, suffix
):
    INPUTDIR = addsep(inputdir)
    OUTPUTDIR = addsep(outputdir)
    os.system("mkdir -p " + OUTPUTDIR)
    os.system("mkdir -p " + OUTPUTDIR + "CHECK")
    TIMELIST = file2stringlist(timelist)
    Mask_bitsea1 = Mask(nativemask)
    Mask1 = mask(nativemask)
    Mask2 = mask(outmaskfile)
    
    for time in TIMELIST[rank::nranks]:
        filename=time[:8] +suffix+ ".nc"
        inputfile = INPUTDIR + filename
        outputfile= OUTPUTDIR + filename
        B = DataExtractor(Mask_bitsea1, inputfile, satvar).values
        M = space_intepolator_griddata(Mask2, Mask1, B)
        writeSatFile(M=M, outputfile=outputfile, var=satvar, Mask1=Mask1, Mask2=Mask2)


if __name__ == "__main__":
    args = argument()
    gen_sat_files(
        inputdir=args.inputdir,
        outputdir=args.outputdir,
        nativemask=args.nativemask,
        timelist=args.timelist,
        outmaskfile=args.outmaskfile,
        satvar=args.satvar,
        suffix=args.suffix
    )
