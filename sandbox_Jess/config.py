#!/usr/bin/env python
import math

files=["root://cmsxrootd.fnal.gov//store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/70000/C6AABB0E-33AC-E811-8B63-0CC47A7C3404.root"]
isMC=True

histFileName_ = None
histDirName_ = None

# ------------------Muon-----------------
muSelCond={}
muSelCond["tightId"] = "> 0"
muSelCond["miniPFRelIso_all"] = "< 0.1"
muSelCond["dxy"] = "< 0.2"
muSelCond["dz"] = "< 0.5"
muSelCond["pt"] = "> 30."
muSelCond["eta"] = "< 2.4"

# ------------------Electron------------------
elSelCond={}
elSelCond["mvaFall17noIso_WP90"] = "> 0"
elSelCond["miniPFRelIso_all"] = "< 0.1"
elSelCond["pt"] = "> 30."
elSelCond["eta"] = "< 2.5"

# # ------------------LepJetCleaning------------------
DoLepJetCleaning = True
LepJetCleaning_DR = 0.4

# # ------------------Jet------------------
killHF=False
jetSelCond={}
jetSelCond["jetId"] = "> 0"
jetP4SelCond={}
jetP4SelCond["Pt"] = "> 20."
jetP4SelCond["Eta"] = "< 2.4"
if killHF:
  jetP4SelCond["Eta"] = "<= 2.4"

# # ------------------AK8Jet------------------
fatJetSelCond = {}
fatJetSelCond["jetId"] = "> 0"
fatJetP4SelCond={}
fatJetP4SelCond["Pt"] = ">= 170."
if killHF:
  fatJetP4SelCond["Eta"] = "<= 2.4"

# ------------------Preselection------------------
Preselection_list = [
	"PV_npvsGood > 0",
	"Flag_METFilters",
	"MET_pt > 30",
	"nJet>=2",
	# "nJet<=999",
	"(nMuon>=1 || nElectron>=1)",
	"nFatJet>=0",
	# "nFatJet<=999"
]

keepPDGID = [1, 2, 3, 4, 5, 6, 21, 11, 12, 13, 14, 15, 16, 24]
keepMomPDGID = [6, 24]
keepPDGIDForce = [6,6]
keepStatusForce = [62,22]
cleanGenJets = True


# ------------------Triggers------------------
MC_trigger_list = [
	"HLT_Ele35_WPTight_Gsf",
	"HLT_Ele38_WPTight_Gsf",
	"HLT_Ele40_WPTight_Gsf",
	"HLT_Ele28_eta2p1_WPTight_Gsf_HT150",
	"HLT_Ele15_IsoVVVL_PFHT450_PFMET50",
	"HLT_Ele15_IsoVVVL_PFHT450",
	"HLT_Ele50_IsoVVVL_PFHT450",
	"HLT_Ele15_IsoVVVL_PFHT600",
	"HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165",
	"HLT_Ele115_CaloIdVT_GsfTrkIdT",
	"HLT_IsoMu24",
	"HLT_IsoMu24_eta2p1",
	"HLT_IsoMu27",
	"HLT_IsoMu30",
	"HLT_Mu50",
	"HLT_Mu55",
	"HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5",
	"HLT_Mu15_IsoVVVL_PFHT450_PFMET50",
	"HLT_Mu15_IsoVVVL_PFHT450",
	"HLT_Mu50_IsoVVVL_PFHT450",
	"HLT_Mu15_IsoVVVL_PFHT600"
]
data_trigger_list = [
	"HLT_Ele35_WPTight_Gsf",
	"HLT_Ele38_WPTight_Gsf",
	"HLT_Ele40_WPTight_Gsf",
	"HLT_Ele28_eta2p1_WPTight_Gsf_HT150",
	"HLT_Ele15_IsoVVVL_PFHT450_PFMET50",
	"HLT_Ele15_IsoVVVL_PFHT450",
	"HLT_Ele50_IsoVVVL_PFHT450",
	"HLT_Ele15_IsoVVVL_PFHT600",
	"HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165",
	"HLT_Ele115_CaloIdVT_GsfTrkIdT",
	"HLT_IsoMu24",
	"HLT_IsoMu24_eta2p1",
	"HLT_IsoMu27",
	"HLT_IsoMu30",
	"HLT_Mu50",
	"HLT_Mu55",
	"HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5",
	"HLT_Mu15_IsoVVVL_PFHT450_PFMET50",
	"HLT_Mu15_IsoVVVL_PFHT450",
	"HLT_Mu50_IsoVVVL_PFHT450",
	"HLT_Mu15_IsoVVVL_PFHT600"
]
