from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from random import randint
from copy import deepcopy

from HelpfulAIs.GeneralUtilsAI import GeneralUtilsAI

class InvalidBuildOrder(Exception): # will be raised any time the build order ain't orderin'
    pass                            # will then be caught in the except below, and we'll switch to non-build-order mode

class BuildingOrderBot(GeneralUtilsAI):
    async def ExecuteBuildOrder(self):
        if self.IsFirstStep:
            self.UsingBuildOrder = True
            
            try:
                self.BuildOrder = GetBuildOrderArray()
                self.BuildOrder = SplitOutMultipleBuildSteps(self.BuildOrder)
                self.BuildOrder = SetChronoBool(self.BuildOrder)
                self.BuildOrder = StandardiseBuildsThatUseXs(self.BuildOrder) #Some steps show things like "Stargate x2". Make that two entries
                self.BuildOrder = TranslateBuildOrderIDs(self.BuildOrder)
                
            except InvalidBuildOrder:
                self.UsingBuildOrder = False
                
            
        if self.UsingBuildOrder:
            pass
        
def StandardiseBuildsThatUseXs(BuildOrder: list[dict]) -> list[dict]:
    for StepIndex, Step in enumerate(BuildOrder):
        if Step["What To Build"][-2] == "x" and Step["What To Build"][-1].isdigit():
            TemporaryStep = BuildOrder.pop(StepIndex)
            TimesToDuplicate = int(TemporaryStep["What To Build"][-1])
            NewWhatToBuild = TemporaryStep["What To Build"][:-2]
            
            for Build in range(0, TimesToDuplicate):
                BuildOrder.insert(StepIndex, deepcopy(TemporaryStep))
                BuildOrder[StepIndex]["What To Build"] = NewWhatToBuild
                
    return BuildOrder

def SplitOutMultipleBuildSteps(BuildOrder: list[dict]) -> list[dict]:
    for StepIndex, Step in enumerate(BuildOrder):
        if "," in Step["What To Build"]:
            BuildsInStep = Step["What To Build"].split(",")
            TemporaryStep = BuildOrder.pop(StepIndex)
            
            for Build in BuildsInStep:
                BuildOrder.insert(StepIndex, deepcopy(TemporaryStep))
                BuildOrder[StepIndex]["What To Build"] = Build.strip()
                
    return BuildOrder
                
            
def SetChronoBool(BuildOrder: list[dict]) -> list[dict]:
    for Step in BuildOrder:
        if "(Chrono Boost)" in Step["What To Build"]:
            Step["Use Chrono"] = True
            Step["What To Build"] = Step["What To Build"].replace("(Chrono Boost)", "")
            Step["What To Build"] = Step["What To Build"].strip()
            
        else: Step["Use Chrono"] = False
    
    return BuildOrder

            
def TranslateBuildOrderIDs(BuildOrder: list[dict]) -> list[dict]: #Take the text (pylon)
    for Step in BuildOrder:
        NextToConstruct = Step["What To Build"].upper().replace(" ", "")

        try:
            Step["What To Build"] = UnitTypeId[NextToConstruct]
        
        except KeyError:
            print(f"Error!! Can't make UnitTypeId from build instruction - issue is in: {Step}")
            raise InvalidBuildOrder
    
    

def GetBuildOrderArray():
    ChosenBuildOrder = SelectBuildOrder()
    
    BuildOrderList = []
    
    for Step in ChosenBuildOrder.splitlines():
        Step = Step.strip()
        Step = Step.split("\t")
    
        try:
            StepDict = {}
            StepDict["Supply Count"] = Step[0].strip()
            StepDict["What To Build"] = Step[2].strip()
        
            BuildOrderList.append(StepDict)
        
        except IndexError:
            pass

    return BuildOrderList

def SelectBuildOrder():
    BuildOrderOptions = [
        """
        13	  0:18	  Pylon	  
        15	  0:37	  Gateway	  
        16	  0:48	  Assimilator	  
        19	  1:22	  Nexus	  
        21	  1:37	  Cybernetics Core	  
        21	  1:45	  Assimilator	  
        22	  1:51	  Pylon	  
        23	  2:15	  Adept
        23	  2:15	  Warp Gate
        26	  2:30	  Pylon	  
        27	  2:37	  Stargate
    """,
    """
        13	  0:18	  Pylon	  
        15	  0:37	  Gateway (Chrono Boost)	  
        16	  0:48	  Assimilator	  
        19	  1:22	  Nexus, Nexus	  
        21	  1:37	  Cybernetics Core	  
        21	  1:45	  Assimilator	  
        22	  1:51	  Pylon	  
        23	  2:15	  Adept, Warp Gate
        26	  2:30	  Pylon x2
        27	  2:37	  Stargate x2
    """]

    ChosenBuildOrder = BuildOrderOptions[randint(0, len(BuildOrderOptions) -1)]
    return BuildOrderOptions[1]