from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2

from timeit import default_timer as timer
from time import time

import math

class GeneralUtilsAI(BotAI):
    def __init__(self):
        self.TimeDict = {}
        self.RunningTimers = {}
        self.CalledCounters = {}
        self.CalledCountersCurrentTotals = {}
        self.LastStepTime = -1
        self.StepCounter = 0
    
    async def PrepareForNextStep(self):
        self.LastStepTime = self.time
    
    @property
    def StepIsFirstStepOfSecond(self):       
        IsFirstStep = int(self.LastStepTime) < int(self.time)
        #print(f"Last Step: {self.LastStepTime}, This Step: {self.time}")
        return IsFirstStep
        
    
    @property
    def MainBase(self) -> Unit:
        if self.townhalls.exists:
            return self.townhalls.closest_to(self.start_location)
        
    @property
    def SecondBase(self) -> Unit:
        if self.townhalls.exists:
            return self.townhalls.sorted_by_distance_to(self.start_location)[1]
    
    @property
    def Bases(self) -> Units:
        return self.townhalls
    
    @property
    def VespeneBuildingUnitTypeID(self) -> str:
        RaceTypes = {
            Race.Protoss: UnitTypeId.ASSIMILATOR,
            Race.Zerg: UnitTypeId.EXTRACTOR,
            Race.Terran: UnitTypeId.REFINERY,
        }
        
        return RaceTypes[self.race]
    
    @property
    def AllMineralPatches(self) -> Units:
        return self.mineral_field
    
    @property
    def AllVespeneGeysers(self) -> Units:
        return self.vespene_geyser
    
    @property
    def AllVespeneBuildings(self) -> Units:
        return self.gas_buildings.filter(lambda Unit: Unit.is_vespene_geyser)
    
    @property
    def OwnedMineralPatches(self) -> Units:
        Minerals = self.GetEmptyUnitsList()
        
        if self.Bases and self.AllMineralPatches:
            for Base in self.Bases:
                Minerals += self.GetBasePatches(Base)
            
            return Minerals
            
    @property
    def OwnedVespeneGeysers(self) -> Units:
        Geysers = self.GetEmptyUnitsList()
        
        if self.Bases and self.AllVespeneGeysers:
            for Base in self.Bases:
                Geysers += self.GetBaseGeysers(Base)
            
            return Geysers
            
    @property
    def OwnedVespeneBuildings(self) -> Units:
        Buildings = self.GetEmptyUnitsList()
        
        if self.Bases and self.AllVespeneBuildings:
            for Base in self.Bases:
                Buildings += self.GetBaseVespeneBuildings(Base)
            
            return Buildings
        
    @property
    def MaxVespeneProduction(self):
        if self.CountUnit(self.VespeneBuildingUnitTypeID): 
            return self.CountUnit(self.VespeneBuildingUnitTypeID) * 3
        else: return 0
        
        
    @property
    def MaxUtilisationWorkers(self) -> int:
        OwnedPatches = self.OwnedMineralPatches
        OwnedVespeneBuildings = self.OwnedVespeneBuildings
        
        Total = 0
        
        if OwnedPatches:
            Total += OwnedPatches.amount * 2
        
        if OwnedVespeneBuildings:
            Total += OwnedVespeneBuildings.amount * 3
                    
        return Total
    
    @property
    def UnbuiltOwnedExtractors(self):
        return self.OwnedVespeneGeysers.filter(lambda Geyser: Geyser.name == "VespeneGeyser" and not self.gas_buildings.closer_than(1, Geyser))
    
    @property
    def NextGeyserToTake(self) -> Unit:     
        UnbuiltOwnedExtractors = self.UnbuiltOwnedExtractors
        
        if UnbuiltOwnedExtractors.amount == 0: return None
        
        return UnbuiltOwnedExtractors.closest_to(self.MainBase)

    
    def IsFirstStepOfMultipleSecond(self, Multiple: int) -> bool:
        if self.StepIsFirstStepOfSecond:
            if int(self.time) % Multiple == 0: return True
            else: return False
        else: return False
    
    def GetEmptyUnitsList(self):
        return Units([], self)
        
    def Has(self, ID: UnitTypeId) -> bool:
        return self.structures.filter(lambda Unit: Unit.type_id == ID).exists  
    
    def GetUnitsFromList(self, ListForConversion: list[Unit]) -> Units:
        return Units(ListForConversion)[0]
    
    def CurrentlyBuilding(self, ID: UnitTypeId = None):
        if UnitTypeId is None:
            return self.structures.filter(lambda Structure: not Structure.is_ready)
        
        else:
            return self.structures.filter(lambda Structure: not Structure.is_ready and Structure.type_id == ID)
            
    def GetVector(self, Source: Unit | Point2, Target: Unit | Point2) -> float:
        if Source and Target:
            SourcePos = self.UnitOrPositionToPosition(Source)
            TargetPos = self.UnitOrPositionToPosition(Target)
                        
            return TargetPos - SourcePos
    
    def NormaliseVector(self, Vector: Point2):
        if Vector:
            return Vector / self.GetVectorLength(Vector)
        
    def InvertVector(self, Vector: Point2):
        return -Vector
    
    def AwayFrom(self, SourceUnit: Unit | Point2, TargetUnit: Unit | Point2, Distance: float = 1) -> Point2:
        Towards = self.GetVector(SourceUnit, TargetUnit)
        TowardsNormalised = self.NormaliseVector(Towards)
        Away = self.InvertVector(TowardsNormalised)
        VectorScaled = Away * Distance
        
        return VectorScaled + self.UnitOrPositionToPosition(SourceUnit)
    
    def GetVectorLength(self, Vector: Point2):
        return math.sqrt((Vector.x * Vector.x) + (Vector.y * Vector.y))
        
        
    def UnitOrPositionToPosition(self, Input: Point2 | Unit) -> Point2:
        if isinstance(Input, Unit):
            return Input.position
        return Input
    
    
    def GetUnitsListFromUnits(self, UnitsGroup) -> list[Unit]:
        if UnitsGroup:
            UnitsList = []
            for Unit in UnitsGroup:
                UnitsList.append(Unit)
            
            return UnitsList
    
    
    def GetBasePatches(self, Base: Unit | Point2) -> Units:
        if Base and self.AllMineralPatches:
            return self.AllMineralPatches.closer_than(10, Base)
        
    def GetBaseGeysers(self, Base: Unit | Point2):
        if Base and self.AllVespeneGeysers:
            return self.AllVespeneGeysers.closer_than(10, Base)
        
    def GetBaseVespeneBuildings(self, Base: Unit | Point2) -> Units:
        if Base and self.AllVespeneBuildings:
            return self.AllVespeneBuildings.closer_than(10, Base)
        
    
    def GetCentreOfBasePatches(self, Base: Unit | Point2) -> Point2:
        NearbyPatches = self.GetBasePatches(Base)
        if Base and NearbyPatches:
            return NearbyPatches.center
        
    
    def CountUnit(self, ID: UnitTypeId) -> int:
        AlreadyPendingUnits = self.already_pending(ID)
        ExistingStructures = self.structures.filter(lambda unit: unit.type_id == ID and unit.is_ready).amount
        ExistingUnits = self.units.filter(lambda unit: unit.type_id == ID and unit.is_ready).amount
        return  AlreadyPendingUnits + ExistingStructures + ExistingUnits
    
    def UsedSupplyBetween(self, Low: int, High: int) -> bool:
        return self.supply_used >= Low and self.supply_used < High 
    
    def TotalSupplyBetween(self, Low: int, High: int) -> bool:
        return self.supply_used >= Low and self.supply_used < High 
    
    def GetDebugInfo(self, PrintOut: bool = False, Frequency: int = 20, Iteration: int = 0):
        self.UpdateAverageTimeDict(PrintOut, Frequency)
        self.UpdateAverageRunsDict(PrintOut, Frequency)
        self.TrackStepLoss(PrintOut, Frequency, Iteration)
        if self.IsFirstStepOfMultipleSecond(Frequency):

            print("\n")
    
    def TrackStepLoss(self, PrintOut: bool = False, Frequency: int = 20, Iteration: int = 0):
        self.StepCounter += 1
        if Iteration > self.StepCounter:
            if self.IsFirstStepOfMultipleSecond(Frequency) and PrintOut:
                print(f"Internal Step Counter ({self.StepCounter}) is less than bot iteration ({Iteration})... ")
            
        
    
    async def TimeIt(self, Function, FunctionName):
        TimeAtStart = timer()
        Result = await Function()
        TimeAtEnd = timer()
        TimeElapsed = TimeAtEnd-TimeAtStart
        
        self.AddToTimedFunctionsDict(FunctionName, TimeElapsed)
        return Result
            
    def AddToTimedFunctionsDict(self, FunctionName, TimeElapsed):
        if not FunctionName in self.TimeDict:
            self.TimeDict[FunctionName] = [TimeElapsed]
        else:
            self.TimeDict[FunctionName].append(TimeElapsed)
        
            
    def UpdateAverageTimeDict(self, PrintOut: bool = False, Frequency: int = 20):       
        if not self.IsFirstStepOfMultipleSecond(Frequency):
            return
        
        self.AverageTimeDict = {}
        
        for Key in self.TimeDict:
            self.AverageTimeDict[Key] = f"{sum(self.TimeDict[Key]) / len(self.TimeDict[Key]):.20f}"
            
        if PrintOut:
            print(f"Average run times at {self.time} seconds:")
            for Key in self.AverageTimeDict:
                Padding = " " * (20 - len(Key))
                print(f"{Key}:{Padding}{self.AverageTimeDict[Key]}")
                
    def UpdateAverageRunsDict(self, PrintOut: bool = False, Frequency: int = 20) -> None:
        if not self.IsFirstStepOfMultipleSecond(Frequency):
            return
        
        self.AverageRunsDict = {}
        
        for Key in self.CalledCounters:
            self.AverageRunsDict[Key] = f"{sum(self.CalledCounters[Key]) / len(self.CalledCounters[Key]):.20f}"
            
        if PrintOut:
            print(f"Average times called per 20 seconds at {self.time} seconds:")
            for Key in self.AverageRunsDict:
                Padding = " " * (20 - len(Key))
                print(f"{Key}:{Padding}{self.AverageRunsDict[Key]}")
                
        self.CalledCounters = {}
            
    def StartTimer(self, Name):
        if Name in self.RunningTimers:
            print("This timer is already running! Stop it first!! Gonna get wrong values...")
        else:
            self.RunningTimers[Name] = time()
            
    def StopTimer(self, Name: str):
        if not Name in self.RunningTimers:
            print("This timer isn't currently running. AAAaaa!")
        
        else:
            CurrentTime = time()
            StartTime = self.RunningTimers.pop(Name)
            ElapsedTime = CurrentTime - StartTime
            
            self.AddToTimedFunctionsDict(Name, ElapsedTime)
            
    def GiveInfrequentDebugUpdates(self, Message: str, Frequency: int = 10) -> None:
        if self.IsFirstStepOfMultipleSecond(Frequency):
            print(Message)
        
    def CountTimesCalledPerPeriod(self, Name: str, Period: int = 20):
        if Name in self.CalledCountersCurrentTotals:
            self.CalledCountersCurrentTotals[Name] += 1
            
        else:
            self.CalledCountersCurrentTotals[Name] = 1
            
        if self.IsFirstStepOfMultipleSecond(Period):
            if Name in self.CalledCounters:
                self.CalledCounters[Name].append(self.CalledCountersCurrentTotals[Name])
            else:
                self.CalledCounters[Name] = [self.CalledCountersCurrentTotals[Name]]
                
            self.CalledCountersCurrentTotals[Name] = 0 
        
