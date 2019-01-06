import os,sys

samplelist = [

	# TTTT
   '/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAOD-PU2017_pilot_94X_mc2017_realistic_v14-v1/NANOAODSIM',


    ]

datalistRRB = [
'/SingleMuon/Run2017B-31Mar2018-v1/NANOAOD',
'/SingleElectron/Run2017B-31Mar2018-v1/NANOAOD',
]
datalistRRC = [
'/SingleMuon/Run2017C-31Mar2018-v1/NANOAOD',
'/SingleElectron/Run2017C-31Mar2018-v1/NANOAOD',
]
datalistRRD = [
'/SingleMuon/Run2017D-31Mar2018-v1/NANOAOD',
'/SingleElectron/Run2017D-31Mar2018-v1/NANOAOD',
]
datalistRRE = [
'/SingleMuon/Run2017E-31Mar2018-v1/NANOAOD',
'/SingleElectron/Run2017E-31Mar2018-v1/NANOAOD',
]
datalistRRF = [
'/SingleMuon/Run2017F-31Mar2018-v1/NANOAOD',
'/SingleElectron/Run2017F-31Mar2018-v1/NANOAOD',
]


for sample in samplelist:
    print 'listing files in',sample
    os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" &>> fileLists/'+sample.split('/')[1]+'.txt')

# for sample in datalistRRB:
#     print 'listing files in',sample
#     os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" >& fileLists/'+sample.split('/')[1]+'_RRB.txt')
# 
# for sample in datalistRRC:
#     print 'listing files in',sample
#     os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" >& fileLists/'+sample.split('/')[1]+'_RRC.txt')
# 
# for sample in datalistRRD:
#     print 'listing files in',sample
#     os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" >& fileLists/'+sample.split('/')[1]+'_RRD.txt')
# 
# for sample in datalistRRE:
#     print 'listing files in',sample
#     os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" >& fileLists/'+sample.split('/')[1]+'_RRE.txt')
# 
# for sample in datalistRRF:
#     print 'listing files in',sample
#     os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" >& fileLists/'+sample.split('/')[1]+'_RRF.txt')
