import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class EventSelector_1Lep(Module):

    def __init__(self):
        print 'Running EventSelector_1Lep module'
        		

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        
        #select based on flags? eg. Flag_METFilters
#         if not ( event.Flag_METFilters ): return False
                
        #select based on PV? eg. PV_npvsGood > 0 
        if not ( event.PV_npvsGood > 0 ): return False

        #select events with at least 1 lepton. Probably can expand to require 1 tight leptons here, also jet requirements 
        if not ( len(muons)+len(electrons) >=1 ): return False

        return True

