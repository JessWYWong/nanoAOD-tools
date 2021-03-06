import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class EventSelector(Module):

    def __init__(self):
        print 'Running EventSelector module'
        		

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        
        #select based on flags? eg. Flag_METFilters
#         if not ( event.Flag_METFilters ): return False
                
        #select based on PV? eg. PV_npvsGood > 0 
        if not ( event.PV_npvsGood > 0 ): return False

        #select events with at least 2 leptons
        if not ( len(muons)+len(electrons) >=2 ): return False

        return True

