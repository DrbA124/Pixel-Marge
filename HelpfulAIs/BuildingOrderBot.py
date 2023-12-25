from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
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
            self._BuildOrderStep = 0
            
            try:
                self.BuildOrder = GetBuildOrderArray()
                self.BuildOrder = RenameMisalignedBuilds(self.BuildOrder) # Some things are misnamed and need to be aligned to our enum
                self.BuildOrder = SplitOutMultipleBuildSteps(self.BuildOrder)
                self.BuildOrder = SetChronoBool(self.BuildOrder)
                self.BuildOrder = StandardiseBuildsThatUseXs(self.BuildOrder) #Some steps show things like "Stargate x2". Make that two entries
                self.BuildOrder = TranslateBuildOrderIDs(self.BuildOrder)
                self.BuildOrder = AddCountDemanded(self.BuildOrder)
                
            except InvalidBuildOrder:
                self.UsingBuildOrder = False
                print("Build order is invalid! Will not use.")
                
            
        if self.UsingBuildOrder:
            await self.ExecuteNextStepOfBuildOrder()
    
    async def ExecuteNextStepOfBuildOrder(self) -> None: 
        Step = self.BuildOrder[self._BuildOrderStep]
        DemandedBuilding = Step["What To Build"]
        NumberDemanded = Step["Number Demanded To Complete Step"]
        MinimumSupplyCountToBuild = Step["Supply Count"]
        
        if self.supply_used < MinimumSupplyCountToBuild:
            return
        
        elif self.CountUnit(DemandedBuilding) >= NumberDemanded:
            self._BuildOrderStep += 1
            return
        
        elif Step["Build Type"] == "Unit":
            await self.BuildUnit(DemandedBuilding)
            
        elif Step["Build Type"] == "Upgrade":
            await self.GetUpgrade(DemandedBuilding)
            
    

def AddCountDemanded(BuildOrder: list[dict]) -> list[dict]:
    for StepIndex, Step in enumerate(BuildOrder):
        BuildDemanded = Step["What To Build"]
        NumberDemanded = 1
        
        for PreviousStepIndexToCheck in range(0, StepIndex):
            PreviousStepToCheck = BuildOrder[PreviousStepIndexToCheck]
            PreviousStepToCheckBuilding = PreviousStepToCheck["What To Build"]
            
            if PreviousStepToCheckBuilding == BuildDemanded:
                NumberDemanded += 1
                
        Step["Number Demanded To Complete Step"] = NumberDemanded
        
    return BuildOrder
        
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

        ValidUnitIDs = [Id.name for Id in UnitTypeId]
        ValidUpgradeIDs = [Id.name for Id in UpgradeId]
        
        if NextToConstruct in ValidUnitIDs:
            Step["What To Build"] = UnitTypeId[NextToConstruct]
            Step["Build Type"] = "Unit"
        
        elif NextToConstruct in ValidUpgradeIDs:
            Step["What To Build"] = UpgradeId[NextToConstruct]
            Step["Build Type"] = "Upgrade"

        else:
            print(f"Error!! Can't make UnitTypeId or UpgradeId from build instruction - issue is in: {Step}")
            raise InvalidBuildOrder
        
    return BuildOrder
    
    

def GetBuildOrderArray():
    ChosenBuildOrder = SelectBuildOrder()
    
    BuildOrderList = []
    
    for Step in ChosenBuildOrder.splitlines():
        Step = Step.strip()
        Step = Step.split("\t")
    
        try:
            StepDict = {}
            StepDict["Supply Count"] = int(Step[0].strip())
            StepDict["What To Build"] = Step[2].strip()
        
            BuildOrderList.append(StepDict)
        
        except IndexError:
            pass

    return BuildOrderList

def RenameMisalignedBuilds(BuildOrder: list[dict]) -> list[dict]:
    for Step in BuildOrder:
        if Step["What To Build"].upper() == "Warp Gate".upper():
            Step["What To Build"] = "Warp Gate Research"
            
    return BuildOrder
        

def SelectBuildOrder():
    BuildOrderOptions = [
        """13	  0:18	  Pylon	  
           15	  0:37	  Gateway	  
           16	  0:48	  Assimilator	  
           19	  1:22	  Nexus	  
           21	  1:37	  Cybernetics Core	  
           21	  1:45	  Assimilator	  
           22	  1:51	  Pylon	  
           23	  2:15	  Adept
           23	  2:15	  Warp Gate Research
           26	  2:30	  Pylon	  
           27	  2:37	  Stargate""",
           
        """13	  0:18	  Pylon	  
           15	  0:37	  Gateway (Chrono Boost)	  
           16	  0:48	  Assimilator	  
           19	  1:22	  Nexus, Nexus	  
           21	  1:37	  Cybernetics Core	  
           21	  1:45	  Assimilator	  
           22	  1:51	  Pylon	  
           23	  2:15	  Adept, Warp Gate Research
           26	  2:30	  Pylon x2
           27	  2:37	  Stargate x2"""
           ]

    ChosenBuildOrder = BuildOrderOptions[randint(0, len(BuildOrderOptions) -1)]
    return BuildOrderOptions[1]