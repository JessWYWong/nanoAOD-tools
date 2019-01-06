#!/bin/bash

#rm -iv /uscms_data/d3/rsyarif/Brown2018/NanoAOD_LJMet/CMSSW_9_4_11.tar

echo "SUBMITTING nAODtoLJMET -- RR 2017Data"

python -u condor_submitData2017.py nominal 

echo "SUBMITTING nAODtoLJMET -- nominal MC"

python -u condor_submitMC2017.py nominal


echo "DONE"
