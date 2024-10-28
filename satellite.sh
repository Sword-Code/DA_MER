
. setup.sh

inputdir=
outputdir=
nativemask=
outmaskfile=
satvar=
suffix=

### this python script will be soon substituted with a more advanced one that also downloads satellite data from copernicus
python interpolate_sat.py --inputdir $inputdir --outmaskfile $outmaskfile --outputdir $outputdir --nativemask $nativemask --satvar $satvar --suffix $suffix --timelist $DAtime_file
