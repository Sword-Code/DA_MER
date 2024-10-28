
. setup.sh

inputdir=
outputdir=
nativemask=
outmaskfile=
satvar=
suffix=

python interpolate_sat.py --inputdir $inputdir --outmaskfile $outmaskfile --outputdir $outputdir --nativemask $nativemask --satvar $satvar --suffix $suffix --timelist $DAtime
