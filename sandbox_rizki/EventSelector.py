import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class EventSelector(Module):

    def __init__(self):
        print 'Running EventSelector module'
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")

        #select events with at least 2 leptons
        if len(muons)+len(electrons) >=2:
            return True
        else:
            return False
