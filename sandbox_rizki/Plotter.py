import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class Plotter(Module):

    def __init__(self):
        print 'Running Plotter module'
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

        self.h_ST=ROOT.TH1F('ST',   'ST',   100, 0, 1000)
        self.addObject(self.h_ST)


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        #define ST based on TestCalc
        ST = event.postNAOD_ST_TestCalc

        self.h_ST.Fill(ST) #fill histogram

        return True
