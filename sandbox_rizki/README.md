
## nAODtoLJMet

### ----------------- Installation -----------------

    source /cvmfs/cms.cern.ch/cmsset_default.csh

    setenv SCRAM_ARCH ' slc6_amd64_gcc630'

    cmsrel CMSSW_9_4_11
    cd CMSSW_9_4_11/src

    git clone -b LJMet_nAOD_94x git@github.com:rsyarif/nanoAOD-tools.git PhysicsTools/NanoAODTools
    cd PhysicsTools/NanoAODTools
    cmsenv
    scram b

everything nAODtoLJMet currently isolated in "sandbox_rizki" since still in development stage.

see example in "example_nAODprocess_rizki_v4.py"

to run example:

   python example_nAODprocess_rizki_v4.py


### condor

see "condor" directory and modify "template_process_nAODtoLJMet.py"
create and modify modules in "ljmet_modules"

check ALL files and modify paths etc correctly, run "submit_nAODtoLJMet.py" to send condor jobs



