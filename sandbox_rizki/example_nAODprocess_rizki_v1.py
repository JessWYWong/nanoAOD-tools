#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class ExampleAnalysis(Module):

    def __init__(self):
    	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
    	Module.beginJob(self,histFile,histDirName)
    	
    	self.h_ST=ROOT.TH1F('ST',   'ST',   100, 0, 1000)
        self.addObject(self.h_ST)
        
#     def endJob(self):
#         pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    
        self.out = wrappedOutputTree
        self.out.branch("postNAODCalc_ST",  "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass    

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")

        event_p4 = ROOT.TLorentzVector()
         
        #select events with at least 2 leptons
        if len(muons)+len(electrons) >=2:
        
			#print "run/lumiblock/event:", int(event.run), int(event.luminosityBlock), long(event.event),"#e:",len(electrons),"#mu:",len(muons)
	
			#loop on muons
			for lep in muons :     
				event_p4 += lep.p4()

			#loop on electrons
			for lep in electrons : 
				event_p4 += lep.p4()
		
			#loop on jets
			for j in jets :       
				event_p4 += j.p4()
				
			#MET
			metPt = event.MET_pt
			
			#define ST
			ST = event_p4.Pt()+metPt
		
			self.h_ST.Fill(ST) #fill histogram
			
			self.out.fillBranch("postNAODCalc_ST",ST) # fill new branch

			return True

        else:
        	
        	return False


preselection="(Jet_pt[0] > 30 && Electron_pt[0] > 40 && Electron_pt[1] > 35 && Muon_pt[0] > 40 && Muon_pt[1] > 35)"

triggers = "(HLT_Mu37_Ele27_CaloIdL_MW==1 || HLT_Mu27_Ele37_CaloIdL_MW==1 || HLT_Mu37_TkMu27==1|| HLT_Ele27_Ele37_CaloIdL_MW==1)"

files=["root://cmsxrootd.fnal.gov//store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/PU2017_pilot_94X_mc2017_realistic_v14-v1/90000/EA11BEB7-B732-E811-A77A-0CC47AA992AC.root"]

p=PostProcessor("nanoAODSkim",
				files,
				cut=preselection+" && "+triggers,
				branchsel="keep_and_drop_input.txt",
				outputbranchsel="keep_and_drop_output.txt",
				modules=[ExampleAnalysis()],
				noOut=False,
				histFileName="histOut.root",
				histDirName="plots")
p.run()
