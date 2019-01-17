import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class CommonCalc(Module):

    def __init__(self):
        print 'Running CommonCalc module'
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        self.out = wrappedOutputTree
        self.out.branch("event_CommonCalc",  "L");
        self.out.branch("run_CommonCalc",  "I");
        self.out.branch("lumi_CommonCalc",  "I");

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        self.out.fillBranch("event_CommonCalc",event.event) # fill new branch
        self.out.fillBranch("run_CommonCalc",event.run) # fill new branch
        self.out.fillBranch("lumi_CommonCalc",event.luminosityBlock) # fill new branch

        return True
