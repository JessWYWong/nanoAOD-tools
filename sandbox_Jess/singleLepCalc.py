import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

# singleLep Calc is not the most appropriate name. Should be called LepCalc, imo.
class singleLepCalc(Module): 

    def __init__(self):
        print 'Running singleLepCalc module'
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        self.out = wrappedOutputTree

        #self.out.branch(nameVar,  typeVar, lenVar); 

		##################################################	
		#Misc
		##################################################	

		#I think these should NOT be in singleLep Calc. Maybe CommonCalc instead.
        self.out.branch("nPV_singleLepCalc",  "I"); 
        self.out.branch("nTrueInteractions_singleLepCalc",  "F"); 
        self.out.branch("MCWeight_singleLepCalc",  "F"); 
        
		##################################################	
		#electrons
		##################################################	

        self.out.branch("elPt_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elEta_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elPFEta_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elPFPhi_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elEnergy_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elMVAValue_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elMiniIso_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elRelIso_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elDxy_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elDZ_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elCharge_singleLepCalc",  "I", lenVar="nElectron"); 
        self.out.branch("elDEtaSCTkAtVtx_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elDR03TkSumPt_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elSihih_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elHoE_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elisTightIso_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elisLooseIso_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elisTight_singleLepCalc",  "F", lenVar="nElectron"); 
        self.out.branch("elisLoose_singleLepCalc",  "F", lenVar="nElectron"); 
        
		##################################################	
		#muons
		##################################################	

        self.out.branch("muPt_singleLepCalc",  "F", lenVar="nMuon"); 
        self.out.branch("muEta_singleLepCalc",  "F", lenVar="nMuon"); 
        self.out.branch("muPhi_singleLepCalc",  "F", lenVar="nMuon"); 
        self.out.branch("muEnergy_singleLepCalc",  "F", lenVar="nMuon"); 
        self.out.branch("muMiniIso_singleLepCalc",  "F", lenVar="nMuon"); 
        self.out.branch("muRelIso_singleLepCalc",  "F", lenVar="nMuon"); 
        self.out.branch("muDxy_singleLepCalc",  "F", lenVar="nMuon"); 
        self.out.branch("muDz_singleLepCalc",  "F", lenVar="nMuon"); 
        self.out.branch("muCharge_singleLepCalc",  "I", lenVar="nMuon"); 
        
		##################################################	
		#MET
		##################################################	

        self.out.branch("corr_met_singleLepCalc",  "F"); 
        self.out.branch("corr_met_phi_singleLepCalc",  "F"); 


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

		##################################################	
		#Misc
		##################################################	

		#I think these should NOT be in singleLep Calc. Maybe CommonCalc instead.
        self.out.fillBranch("nPV_singleLepCalc",event.PV_npvsGood) 
        
        #skip below if doesn exist (for Data)
        try:
        	self.out.fillBranch("nTrueInteractions_singleLepCalc",event.Pileup_nTrueInt) 
        	self.out.fillBranch("MCWeight_singleLepCalc",event.Generator_weight)
        except:
        	pass

		##################################################	
		#electrons
		##################################################	
		
		#calculate new variabes
        electrons = Collection(event, "Electron")
        el_p4 = ROOT.TLorentzVector()
        el_Eta = []
        el_E = []
        for electron in electrons:
        	el_p4 = electron.p4()
        	el_Eta.append(electron.eta + electron.deltaEtaSC)
        	el_E.append(el_p4.E())
        
        #fill branches
        self.out.fillBranch("elPt_singleLepCalc",event.Electron_pt) 
        self.out.fillBranch("elEta_singleLepCalc",el_Eta) 
        self.out.fillBranch("elPFEta_singleLepCalc",event.Electron_eta) 
        self.out.fillBranch("elPFPhi_singleLepCalc",event.Electron_phi) 
        self.out.fillBranch("elEnergy_singleLepCalc",el_E) 
#         self.out.fillBranch("elMVAValue_singleLepCalc",event.Electron_mvaFall17noIso) #doesn exist in current nanoAOD file
        self.out.fillBranch("elMiniIso_singleLepCalc",event.Electron_miniPFRelIso_all) 
        self.out.fillBranch("elRelIso_singleLepCalc",event.Electron_pfRelIso03_all) 
        self.out.fillBranch("elDxy_singleLepCalc",event.Electron_dxy) 
        self.out.fillBranch("elDZ_singleLepCalc",event.Electron_dz) 
        self.out.fillBranch("elCharge_singleLepCalc",event.Electron_charge) 
        self.out.fillBranch("elDEtaSCTkAtVtx_singleLepCalc",event.Electron_deltaEtaSC) 
        self.out.fillBranch("elDR03TkSumPt_singleLepCalc",event.Electron_dr03TkSumPt) 
        self.out.fillBranch("elSihih_singleLepCalc",event.Electron_sieie) 
        self.out.fillBranch("elHoE_singleLepCalc",event.Electron_hoe) 
#         self.out.fillBranch("elisTightIso_singleLepCalc",event.Electron_mvaFall17Iso_WP90) #doesn exist in current nanoAOD file
#         self.out.fillBranch("elisLooseIso_singleLepCalc",event.Electron_mvaFall17Iso_WPL) #doesn exist in current nanoAOD file
#         self.out.fillBranch("elisTight_singleLepCalc",event.Electron_mvaFall17noIso_WP90) #doesn exist in current nanoAOD file
#         self.out.fillBranch("elisLoose_singleLepCalc",event.Electron_mvaFall17noIso_WPL) #doesn exist in current nanoAOD file
        
		##################################################	
		#muons
		##################################################	

		#calculate new variabes
        muons = Collection(event, "Muon")
        mu_p4 = ROOT.TLorentzVector()
        mu_E = []
        for muon in muons:
        	mu_p4 = muon.p4()
        	mu_E.append(mu_p4.E())
        
        #fill branches
        self.out.fillBranch("muPt_singleLepCalc",event.Muon_pt) 
        self.out.fillBranch("muEta_singleLepCalc",event.Muon_eta) 
        self.out.fillBranch("muPhi_singleLepCalc",event.Muon_phi) 
        self.out.fillBranch("muEnergy_singleLepCalc",mu_E) 
        self.out.fillBranch("muMiniIso_singleLepCalc",event.Muon_miniPFRelIso_all) 
        self.out.fillBranch("muRelIso_singleLepCalc",event.Muon_pfRelIso03_all) 
        self.out.fillBranch("muDxy_singleLepCalc",event.Muon_dxy) 
        self.out.fillBranch("muDz_singleLepCalc",event.Muon_dz) 
        self.out.fillBranch("muCharge_singleLepCalc",event.Muon_charge) 


		##################################################	
		#MET
		##################################################	
		
        self.out.fillBranch("corr_met_singleLepCalc",event.MET_pt) 
        self.out.fillBranch("corr_met_phi_singleLepCalc",event.MET_phi) 
		

        return True
