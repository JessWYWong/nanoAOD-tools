import os,sys,datetime

sampleList=[
	# Should be at CERN, use eoscms.cern.ch in condor_submit.py

# 	'SingleMuon_RRB.txt',
# 	'SingleMuon_RRC.txt',
# 	'SingleMuon_RRD.txt',
# 	'SingleMuon_RRE.txt',
# 	'SingleMuon_RRF.txt',

# 	'SingleElectron_RRB.txt',
# 	'SingleElectron_RRC.txt',
# 	'SingleElectron_RRD.txt',
# 	'SingleElectron_RRE.txt',
# 	'SingleElectron_RRF.txt',
	'SingleElectron_RRF_TEST.txt',

]

shift = sys.argv[1]

print '====== nAODtoLJMET SUBMISSION ======'
	
relBase = os.environ['CMSSW_BASE']
print 'Relbase:',relBase

thisDir = relBase+'/src/PhysicsTools/NanoAODTools/sandbox_rizki/condor/' 
tarfile = relBase+'.tar'
print 'Making tar:'
if os.path.exists(tarfile):
	print 'tar already exists! Will not re-tar!'
else: 
	os.chdir(relBase)
	os.chdir('../')
	print 
	os.system('tar --exclude="src/.git" --exclude="src/fromJess" --exclude="tmp" --exclude="*.SCRAM" --exclude="src/PhysicsTools/NanoAODTools/.git" -zvcf '+tarfile+' '+relBase.split('/')[-1]+'/src/*') #only tar on the level where PhysicsTools is
	os.chdir(thisDir)

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
outdir = 'Testing_nAODtoLJMet_2017datasets_'+date+'_rizki'

for sample in sampleList:
	accessor = 'cmsxrootd.fnal.gov'
	os.system('python condor_submit.py --useMC False --sample '+sample.split('.')[0]+' --json Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt --fileList '+thisDir+'fileLists/'+sample+' --submit True --inputTar '+tarfile+' --outDir /eos/uscms/store/user/lpcljm/'+outdir+' --shift '+shift+' --accessor '+accessor)
