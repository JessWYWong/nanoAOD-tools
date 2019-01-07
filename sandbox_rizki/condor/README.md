

in condor_submit.py modify "tempdir" for saving condor jobs files and logs (its recommended to save outside of CMSSW area)

in condor_submit2017Data/MC.py modify "sampleList" and "outdir" (output will be /store/group/lpcljm/<outdir>)

modify template_process_nAODtoLJMet.py as needed

modify keep_drop_ files as needed

create / select modules from ljmet_modules in parent directory

after all configured, run:

	source submit_nAODtoLJMet.sh

	or (if file mode is set, ie. chmod +x)

	./submit_nAODtoLJMet.sh







