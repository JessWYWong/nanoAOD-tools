import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class TestCalc(Module):

    def __init__(self):
        print 'Running TestCalc module'
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        self.out = wrappedOutputTree
        self.out.branch("postNAOD_ST_TestCalc",  "F");

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")

        event_p4 = ROOT.TLorentzVector()

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

        self.out.fillBranch("postNAOD_ST_TestCalc",ST) # fill new branch

        return True
