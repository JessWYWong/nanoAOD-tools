import os,sys,datetime

shift = sys.argv[1]

sampleList=[

# 	'TESTFILE.txt'
# 	'TESTFILE_2.txt'

	###SIGNAL:
# 	'TTTT_TuneCP5_13TeV-amcatnlo-pythia8.txt', 
	'TTTT_TuneCP5_13TeV-amcatnlo-pythia8_TEST.txt', 

	###BKG:
# 	'WW_TuneCP5_13TeV-pythia8.txt',
# 	'WZTo3LNu_13TeV-powheg-pythia8.txt',
# 	'ZZTo4L_13TeV_powheg_pythia8.txt',

	
	#Additionally for multilepton:
# 	'WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8.txt',
# 	'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8.txt',
# 	'WZZ_TuneCP5_13TeV-amcatnlo-pythia8.txt',
# 	'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8.txt',       
# 						
# 	'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8.txt',       
# 	'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8.txt',			  

	]

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
	os.system('python condor_submit.py --useMC True --sample '+sample.split('.')[0]+' --fileList '+thisDir+'fileLists/'+sample+' --submit True --inputTar '+tarfile+' --outDir /eos/uscms/store/user/lpcljm/'+outdir+' --shift '+shift+' --accessor '+accessor)

## shift should be (one at a time): nominal, JECup, JECdown, JERup, JERdown
## If you want to use different directory names, edit lines 144 - 147 in condor_submit.py so the config is edited correctly
