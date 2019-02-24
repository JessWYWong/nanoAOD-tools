#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math

class TpTpCalc(Module):
  def __init__(self):
    # print 'Running TpTpCalc module'
    pass
  
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    self.out.branch("isBHBH_TpTpCalc", "B")
    self.out.branch("isBHTW_TpTpCalc", "B")
    self.out.branch("isBWBW_TpTpCalc", "B")
    self.out.branch("isBZBH_TpTpCalc", "B")
    self.out.branch("isBZBZ_TpTpCalc", "B")
    self.out.branch("isBZTW_TpTpCalc", "B")
    self.out.branch("isTHBW_TpTpCalc", "B")
    self.out.branch("isTHTH_TpTpCalc", "B")
    self.out.branch("isTWTW_TpTpCalc", "B")
    self.out.branch("isTZBW_TpTpCalc", "B")
    self.out.branch("isTZTH_TpTpCalc", "B")
    self.out.branch("isTZTZ_TpTpCalc", "B")
    self.out.branch("tPrimeStatus_TpTpCalc", "I", lenVar="nGenPart")
    self.out.branch("tPrimeID_TpTpCalc", "I", lenVar="nGenPart")
    self.out.branch("tPrimeMass_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("tPrimePt_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("tPrimeEta_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("tPrimePhi_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("tPrimeEnergy_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("tPrimeNDaughters_TpTpCalc", "I", lenVar="nGenPart")
    self.out.branch("bPrimeStatus_TpTpCalc", "I", lenVar="nGenPart")
    self.out.branch("bPrimeID_TpTpCalc", "I", lenVar="nGenPart")
    self.out.branch("bPrimeMass_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("bPrimePt_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("bPrimeEta_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("bPrimePhi_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("bPrimeEnergy_TpTpCalc", "F", lenVar="nGenPart")
    self.out.branch("bPrimeNDaughters_TpTpCalc", "I", lenVar="nGenPart")
    self.out.branch("NLeptonDecays_TpTpCalc", "I")

  def beginJob(self,histFile=None,histDirName=None):    
    Module.beginJob(self,histFile,histDirName)

  def analyze(self, event):
    genparts = list(Collection(event, "GenPart"))

    isBHBH=False
    isBHTW=False
    isBWBW=False
    isBZBH=False
    isBZBZ=False
    isBZTW=False
    isTHBW=False
    isTHTH=False
    isTWTW=False
    isTZBW=False
    isTZTH=False
    isTZTZ=False
    quarks = []
    bosons = []
    tPrimeStatus = []
    tPrimeID = []
    tPrimeMass = []
    tPrimePt = []
    tPrimeEta = []
    tPrimePhi = []
    tPrimeEnergy = []
    tPrimeNDaughters = []
    bPrimeStatus = []
    bPrimeID = []
    bPrimeMass = []
    bPrimePt = []
    bPrimeEta = []
    bPrimePhi = []
    bPrimeEnergy = []
    bPrimeNDaughters = []
    NLeptonDecays = 0

    for Idx,part in enumerate(genparts):
      partp4 = part.p4()
      if not (abs(part.pdgId) == 8000001 or abs(part.pdgId) == 8000002):
        continue
      hasTdaughter = False
      daughters = []
      daughters = event.genPartDaughters[Idx]
      for dauIdx,dau in daughters:
        if abs(part.pdgId) == 8000001 and abs(dau.pdgId) == 8000001:
          hasTdaughter = True
        if abs(part.pdgId) == 8000002 and abs(dau.pdgId) == 8000002:
          hasTdaughter = True
      if hasTdaughter:
        continue

      mIdx = part.genPartIdxMother
      mother = genparts.__getitem__(mIdx)
      motherp4 = mother.p4()
      mdaughters = []
      mdaughters = event.genPartDaughters[mIdx]
      if abs(part.pdgId) == 8000001:
        if abs(mother.pdgId) == 8000001:
          tPrimeStatus.append(mother.status)
          tPrimeID.append(mother.pdgId)
          tPrimeMass.append(mother.mass)
          tPrimePt.append(mother.pt)
          tPrimeEta.append(mother.eta)
          tPrimePhi.append(mother.phi)
          tPrimeEnergy.append(motherp4.E())
          tPrimeNDaughters.append(len(mdaughters))
        else:
          tPrimeStatus.append(part.status)
          tPrimeID.append(part.pdgId)
          tPrimeMass.append(part.mass)
          tPrimePt.append(part.pt)
          tPrimeEta.append(part.eta)
          tPrimePhi.append(part.phi)
          tPrimeEnergy.append(partp4.E())
          tPrimeNDaughters.append(len(daughters))
      if abs(part.pdgId) == 8000002:
        if abs(mother.pdgId) == 8000002:
          bPrimeStatus.append(mother.status)
          bPrimeID.append(mother.pdgId)
          bPrimeMass.append(mother.mass)
          bPrimePt.append(mother.pt)
          bPrimeEta.append(mother.eta)
          bPrimePhi.append(mother.phi)
          bPrimeEnergy.append(motherp4.E())
          bPrimeNDaughters.append(len(mdaughters))
        else:
          bPrimeStatus.append(part.status)
          bPrimeID.append(part.pdgId)
          bPrimeMass.append(part.mass)
          bPrimePt.append(part.pt)
          bPrimeEta.append(part.eta)
          bPrimePhi.append(part.phi)
          bPrimeEnergy.append(partp4.E())
          bPrimeNDaughters.append(len(daughters))

      for dauIdx,dau in daughters:
        print dau.pdgId
        if abs(dau.pdgId) == 5 or abs(dau.pdgId) == 6:
          quarks.append([dauIdx,dau])
          if abs(dau.pdgId) == 6:
            tdaughters = []
            tdaughters = event.genPartDaughters[dauIdx]
            for tdauIdx,tdau in tdaughters:
              if abs(tdau.pdgId)==6:
                t2daughters = []
                t2daughters = event.genPartDaughters[tdauIdx]
                for t2dauIdx,t2dau in t2daughters:
                  if abs(t2dau.pdgId)==24:
                    Wdaughters = []
                    Wdaughters = event.genPartDaughters[t2dauIdx]
                    for WdauIdx,Wdau in Wdaughters:
                      if abs(Wdau.pdgId) == 24:
                        W2daughters = []
                        W2daughters = event.genPartDaughters[WdauIdx]
                        for W2dauIdx,W2dau in W2daughters:
                          if abs(W2dau.pdgId) == 11 or abs(W2dau.pdgId) == 13 or abs(W2dau.pdgId) == 15:
                            NLeptonDecays += 1
                      if abs(Wdau.pdgId) == 11 or abs(Wdau.pdgId) == 13 or abs(Wdau.pdgId) == 15:
                        NLeptonDecays += 1
              if abs(tdau.pdgId) == 24:
                Wdaughters = []
                Wdaughters = event.genPartDaughters[tdauIdx]
                for WdauIdx,Wdau in Wdaughters:
                  if abs(Wdau.pdgId) == 24:
                    W2daughters = []
                    W2daughters = event.genPartDaughters[WdauIdx]
                    for W2dauIdx,W2dau in W2daughters:
                      if abs(W2dau.pdgId) == 11 or abs(W2dau.pdgId) == 13 or abs(W2dau.pdgId) == 15:
                        NLeptonDecays += 1
                  if abs(Wdau.pdgId) == 11 or abs(Wdau.pdgId) == 13 or abs(Wdau.pdgId) == 15:
                     NLeptonDecays += 1
        elif abs(dau.pdgId) > 22 and abs(dau.pdgId) < 26:
          bosons.append([dauIdx,dau])
          if abs(dau.pdgId) == 24:
            Wdaughters = []
            Wdaughters = event.genPartDaughters[dauIdx]
            for WdauIdx,Wdau in Wdaughters:
              if abs(Wdau.pdgId) == 24:
                W2daughters = []
                W2daughters = event.genPartDaughters[WdauIdx]
                for W2dauIdx,W2dau in W2daughters:
                  if abs(W2dau.pdgId) == 11 or abs(W2dau.pdgId) == 13 or abs(W2dau.pdgId) == 15:
                    NLeptonDecays += 1
              elif abs(Wdau.pdgId) == 11 or abs(Wdau.pdgId) == 13 or abs(Wdau.pdgId) == 15:
                NLeptonDecays += 1
          elif abs(dau.pdgId) == 23:
            Zdaughters = []
            Zdaughters = event.genPartDaughters[dauIdx]
            for ZdauIdx,Zdau in Zdaughters:
              if abs(Zdau.pdgId) == 23:
                Z2daughters = []
                Z2daughters = event.genPartDaughters[ZdauIdx]
                for Z2dauIdx,Z2dau in Z2daughters:
                  if abs(Z2dau.pdgId) == 23:
                    print '!!!TpTpCalc: Z->Z->Z !!!!'
                  elif abs(Z2dau.pdgId) == 11 or abs(Z2dau.pdgId) == 13 or abs(Z2dau.pdgId) == 15:
                    NLeptonDecays += 1
              elif abs(Zdau.pdgId) == 11 or abs(Zdau.pdgId) == 13 or abs(Zdau.pdgId) == 15:
                NLeptonDecays += 1
          elif abs(dau.pdgId) == 25:
            Hdaughters = []
            Hdaughters = event.genPartDaughters[dauIdx]
            for HdauIdx,Hdau in Hdaughters:
              if abs(Hdau.pdgId) == 25:
                H2daughters = []
                H2daughters = event.genPartDaughters[HdauIdx]
                for H2dauIdx,H2dau in H2daughters:
                  if abs(H2dau.pdgId) == 25:
                    print '!!!TpTpCalc: H->H->H !!!!'
                  elif abs(H2dau.pdgId) == 11 or abs(H2dau.pdgId) == 13 or abs(H2dau.pdgId) == 15:
                    NLeptonDecays += 1
              elif abs(Hdau.pdgId) == 11 or abs(Hdau.pdgId) == 13 or abs(Hdau.pdgId) == 15:
                NLeptonDecays += 1
        else:
          continue

    if len(tPrimeID) > 0 and len(bPrimeID) > 0:
      print 'Found both T and B'
    if not (len(quarks) ==0 or len(quarks)==2):
      print 'More/less than 2 quarks stored: '+str(len(quarks))
      for i,quark in (quarks):
        qurakIdx = quark[0]
        q = quark[1]
        print 'quark '+i + ' = ' + q.pdgId
      test = quarks[0][1].pdgId*quarks[1][1].pdgId
      sign = -1
      if test > 0:
        sign = 1
      if sign > 0:
        if len(quarks) == 4:
          quarks[2], quarks[3] = quarks[3], quarks[2]
        quarks[1], quarks[2] = quarks[2], quarks[1]
        test = quarks[0][1].pdgId*quarks[1][1].pdgId
        sign = -1
        if sign < 0:
          print 'Signs are fixed'
      if len(quarks)> 3 and abs(quarks[3][1].pdgId) == 6 :
        quarks[2], quarks[3] = quarks[3], quarks[2]
      if len(quarks)> 2 and abs(quarks[2][1].pdgId) == 6 :
        quarks[1], quarks[2] = quarks[2], quarks[1]
    if not (len(bosons) ==0 or len(bosons)==2):
      print 'More/less than 2 bosons stored: '+str(len(bosons))

    if len(tPrimeID) > 1 and len(bPrimeID) == 0:
      if abs(quarks[0][1].pdgId) == 5 and abs(quarks[1][1].pdgId) ==5 :
        if abs(bosons[0][1].pdgId) == 24 and abs(bosons[1][1].pdgId) ==24 :
          isBWBW = True
      elif abs(quarks[0][1].pdgId) == 6 and abs(quarks[1][1].pdgId) ==6 :
        if abs(bosons[0][1].pdgId) == 23 and abs(bosons[1][1].pdgId) ==23 :
          isTZTZ = True
        elif abs(bosons[0][1].pdgId) == 25 and abs(bosons[1][1].pdgId) ==25 :
          isTHTH = True
        elif (abs(bosons[0][1].pdgId) == 23 and abs(bosons[1][1].pdgId) ==25) or (abs(bosons[0][1].pdgId) == 25 and abs(bosons[1][1].pdgId) ==23):
          isTZTH = True
      elif abs(quarks[0][1].pdgId) == 6 and abs(quarks[1][1].pdgId) ==5 :
        if abs(bosons[0][1].pdgId) == 23 and abs(bosons[1][1].pdgId) ==24:
          isTZBW = True
        elif abs(bosons[0][1].pdgId) == 25 and abs(bosons[1][1].pdgId) ==24:
          isTHBW = True
      elif abs(quarks[0][1].pdgId) == 5 and abs(quarks[1][1].pdgId) ==6 :
        if abs(bosons[0][1].pdgId) == 24 and abs(bosons[1][1].pdgId) ==23:
          isTZBW = True
        elif abs(bosons[0][1].pdgId) == 24 and abs(bosons[1][1].pdgId) ==25:
          isTHBW = True
      else:
        print "T' daughters didn't match a recognized pattern"
    if len(tPrimeID) == 0 and len(bPrimeID) > 1:
      if abs(quarks[0][1].pdgId) == 6 and abs(quarks[1][1].pdgId) ==6:
        if abs(bosons[0][1].pdgId) == 24 and abs(bosons[1][1].pdgId) ==24 :
          isTWTW = True
      elif abs(quarks[0][1].pdgId) == 5 and abs(quarks[1][1].pdgId) ==5 :
        if abs(bosons[0][1].pdgId) == 23 and abs(bosons[1][1].pdgId) ==23 :
          isBZBZ = True
        elif abs(bosons[0][1].pdgId) == 25 and abs(bosons[1][1].pdgId) ==25 :
          isBHBH = True
        elif (abs(bosons[0][1].pdgId) == 23 and abs(bosons[1][1].pdgId) ==25) or (abs(bosons[0][1].pdgId) == 25 and abs(bosons[1][1].pdgId) ==23):
          isBZBH = True
      elif abs(quarks[0][1].pdgId) == 5 and abs(quarks[1][1].pdgId) ==6 :
        if abs(bosons[0][1].pdgId) == 23 and abs(bosons[1][1].pdgId) ==24:
          isBZTW = True
        elif abs(bosons[0][1].pdgId) == 25 and abs(bosons[1][1].pdgId) ==24:
          isBHTW = True
      elif abs(quarks[0][1].pdgId) == 6 and abs(quarks[1][1].pdgId) ==5 :
        if abs(bosons[0][1].pdgId) == 24 and abs(bosons[1][1].pdgId) ==23:
          isBZTW = True
        elif abs(bosons[0][1].pdgId) == 24 and abs(bosons[1][1].pdgId) ==25:
          isBHTW = True
      else:
        print "B' daughters didn't match a recognized pattern"

    self.out.fillBranch("isBHBH_TpTpCalc", isBHBH)
    self.out.fillBranch("isBHTW_TpTpCalc", isBHTW)
    self.out.fillBranch("isBWBW_TpTpCalc", isBWBW)
    self.out.fillBranch("isBZBH_TpTpCalc", isBZBH)
    self.out.fillBranch("isBZBZ_TpTpCalc", isBZBZ)
    self.out.fillBranch("isBZTW_TpTpCalc", isBZTW)
    self.out.fillBranch("isTHBW_TpTpCalc", isTHBW)
    self.out.fillBranch("isTHTH_TpTpCalc", isTHTH)
    self.out.fillBranch("isTWTW_TpTpCalc", isTWTW)
    self.out.fillBranch("isTZBW_TpTpCalc", isTZBW)
    self.out.fillBranch("isTZTH_TpTpCalc", isTZTH)
    self.out.fillBranch("isTZTZ_TpTpCalc", isTZTZ)
    self.out.fillBranch("tPrimeStatus_TpTpCalc", tPrimeStatus)
    self.out.fillBranch("tPrimeID_TpTpCalc", tPrimeID)
    self.out.fillBranch("tPrimeMass_TpTpCalc", tPrimeMass)
    self.out.fillBranch("tPrimePt_TpTpCalc", tPrimePt)
    self.out.fillBranch("tPrimeEta_TpTpCalc", tPrimeEta)
    self.out.fillBranch("tPrimePhi_TpTpCalc", tPrimePhi)
    self.out.fillBranch("tPrimeEnergy_TpTpCalc", tPrimeEnergy)
    self.out.fillBranch("tPrimeNDaughters_TpTpCalc", tPrimeNDaughters)
    self.out.fillBranch("bPrimeStatus_TpTpCalc", bPrimeStatus)
    self.out.fillBranch("bPrimeID_TpTpCalc", bPrimeID)
    self.out.fillBranch("bPrimeMass_TpTpCalc", bPrimeMass)
    self.out.fillBranch("bPrimePt_TpTpCalc", bPrimePt)
    self.out.fillBranch("bPrimeEta_TpTpCalc", bPrimeEta)
    self.out.fillBranch("bPrimePhi_TpTpCalc", bPrimePhi)
    self.out.fillBranch("bPrimeEnergy_TpTpCalc", bPrimeEnergy)
    self.out.fillBranch("bPrimeNDaughters_TpTpCalc", bPrimeNDaughters)
    self.out.fillBranch("NLeptonDecays_TpTpCalc", NLeptonDecays)

    return True



