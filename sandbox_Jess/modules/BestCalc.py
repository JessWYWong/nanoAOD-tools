import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class BestCalc(Module):
  def __init__(self):
    print 'Running Dummy BestCalc'
    pass

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree

    self.out.branch("dnn_QCD_BestCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("dnn_Top_BestCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("dnn_Higgs_BestCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("dnn_Z_BestCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("dnn_W_BestCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("dnn_B_BestCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("dnn_largest_BestCalc", "F", lenVar="nSeljetAK8")


  def analyze(self, event):
    """process event, return True (go to next module) or False (fail, go to next event)"""
    #dummy_vec = []
    #dummy_vec = [0.]*event.nSeljetAK8

    #self.out.branch("dnn_QCD_BestCalc", dummy_vec)
    #self.out.branch("dnn_Top_BestCalc", dummy_vec)
    #self.out.branch("dnn_Higgs_BestCalc", dummy_vec)
    #self.out.branch("dnn_Z_BestCalc", dummy_vec)
    #self.out.branch("dnn_W_BestCalc", dummy_vec)
    #self.out.branch("dnn_B_BestCalc", dummy_vec)
    #self.out.branch("dnn_largest_BestCalc", dummy_vec)

    return True

