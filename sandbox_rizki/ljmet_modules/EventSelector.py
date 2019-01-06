import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class EventSelector(Module):

    def __init__(self):
        print 'Running EventSelector module'
        
        self.pass_METFilters = 0
        self.pass_GoodnPV = 0
        self.pass_nLep = 0
        

	def beginJob(self):
		pass
		

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        
        #select based on flags? eg. Flag_METFilters
#         if not ( event.Flag_METFilters ): return False
#         self.pass_METFilters +=1
                
        #select based on PV? eg. PV_npvsGood > 0 
        if not ( event.PV_npvsGood > 0 ): return False
        self.pass_GoodnPV +=1

        #select events with at least 2 leptons
        if not ( len(muons)+len(electrons) >=2 ): return False
        self.pass_nLep +=1

        return True

	def endJob(self):
	
		#not printing for some reason?
		print "\nEvent Selector:\n"
# 		print "pass_METFilters \t",self.pass_METFilters
		print "pass_GoodnPV \t",self.pass_GoodnPV
		print "pass_nLep \t",self.pass_nLep
