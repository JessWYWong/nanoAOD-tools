import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class DeepAK8Calc(Module):
  def __init__(self):
    print 'Running Dummy DeepAK8Calc'
    pass

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree

    self.out.branch("dnn_B_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("dnn_J_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("dnn_W_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("dnn_Z_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("dnn_H_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("dnn_largest_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("decorr_largest_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("dnn_T_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("decorr_B_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("decorr_J_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("decorr_W_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("decorr_Z_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("decorr_H_DeepAK8Calc", "F", lenVar= "nSeljetAK8")
    self.out.branch("decorr_T_DeepAK8Calc", "F", lenVar= "nSeljetAK8")

  def analyze(self, event):
    """process event, return True (go to next module) or False (fail, go to next event)"""
    #dummy_vec = []
    #dummy_vec = [0.]*event.nSeljetAK8

    #self.out.fillBranch("dnn_B_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("dnn_J_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("dnn_W_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("dnn_Z_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("dnn_H_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("dnn_largest_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("decorr_largest_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("dnn_T_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("decorr_B_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("decorr_J_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("decorr_W_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("decorr_Z_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("decorr_H_DeepAK8Calc", dummy_vec)
    #self.out.fillBranch("decorr_T_DeepAK8Calc", dummy_vec)

    return True
