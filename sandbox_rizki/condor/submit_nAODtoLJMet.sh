#!/bin/bash

echo "SUBMITTING LJMET -- RR 2017Data"

cp TTtrilep_Data_cfg.py ljmet_cfg.py

python -u condor_submitData2017.py nominal | tee submit_Data2017.log 

# echo "SUBMITTING LJMET -- nominal MC"
# 
# cp -v TTtrilep_MC_cfg.py ljmet_cfg.py
# 
# python -u condor_submitMC2017.py nominal | tee submit_MC2017_nominal.log 


echo "DONE"
