from sc2 import maps
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2
from sc2.unit import Unit

from HelpfulAIs.ProtossUtilsAI import ProtossUtilsAI


class BuildingBot(ProtossUtilsAI):
    @property
    def RunningLowOnPlacementSpace(self):
        #Return to this!
        return False
    
    @property
    def RedSupply(self):
        return self.supply_left < 0
    
    @property
    def BasesExist(self):
        return self.townhalls.exists
    
    @property
    def RunningLowOnSupply(self):
        PendingPylons = self.already_pending(UnitTypeId.PYLON)
        
        if self.supply_cap >= 200: return False
        
        #If we're already building pylons, only allow to build more if...
        elif PendingPylons > 0:
            if self.RedSupply and (PendingPylons * 8) < ((-1 * self.supply_left) + 10): return True
            if self.UsedSupplyBetween(100, 200) and PendingPylons < 3 and self.supply_left < 10: return True
            else: return False
            
        elif self.supply_cap >= 200: return False
        elif self.UsedSupplyBetween(0, 20) and self.supply_left < 3: return True
        elif self.UsedSupplyBetween(20, 80) and self.supply_left < 10: return True
        elif self.UsedSupplyBetween(80, 150) and self.supply_left < 20: return True
        elif self.UsedSupplyBetween(150, 200) and self.supply_left < 40: return True
        else: return False
    
    @property
    def NeedMorePylons(self):
        #Probably the most principled way to decide how many pylons we need is to construct supply ranges and desired pylon counts for that range
        #Instead we've got this!
        if not self.BasesExist: return False
        
        if self.RunningLowOnPlacementSpace: return True
        if self.RunningLowOnSupply: return True
        
        return False
    
    @property
    def NeedMoreGateways(self):
        if not self.CountUnit(UnitTypeId.PYLON) >= 1: return False
        
        TotalGates = self.CountUnit(UnitTypeId.WARPGATE) + self.CountUnit(UnitTypeId.GATEWAY)
        NexusCount = self.CountUnit(UnitTypeId.NEXUS)

        if NexusCount == 0:
            return False
        elif NexusCount == 1:
            GatesNeeded = 1
        elif NexusCount == 2:
            GatesNeeded = 4
        elif NexusCount == 2 and self.CountUnit(UnitTypeId.PROBE) > 40:
            GatesNeeded = 8
        elif NexusCount > 2:
            GatesNeeded = 10 + NexusCount
        
        return TotalGates < GatesNeeded 
        
    
    @property
    def NeedMoreExpansions(self):
        #We can calculate if we have a surplus of workers by comparing number of workers to number of owned mineral patches & working geysers
        if self.already_pending(UnitTypeId.NEXUS): return False
        
        NeededWorkers = self.MaxUtilisationWorkers
        ActualWorkers = self.supply_workers
        
        if ActualWorkers and NeededWorkers:
            if ActualWorkers + 5 > NeededWorkers:
                return True
            
    @property
    def NeedCybercore(self):
        if self.CountUnit(UnitTypeId.CYBERNETICSCORE) < 1 and self.CountUnit(UnitTypeId.GATEWAY) >= 1:
            return True
        else:
            return False
        
    @property
    def NeedVespeneBuildings(self):
        MaxProd = self.MaxVespeneProduction
        
        if self.UsedSupplyBetween(0, 17): return False
        elif self.UsedSupplyBetween(100, 200): return True
        
        elif self.UsedSupplyBetween(17, 21) and MaxProd < 3: return True
        elif self.UsedSupplyBetween(21, 48) and MaxProd < 6: return True
        elif self.UsedSupplyBetween(48, 60) and MaxProd < 9: return True
        elif self.UsedSupplyBetween(60, 100) and MaxProd < 12: return True
        else: return False
    
    
    def GetSpotForPylon(self):      
        for Base in self.Bases:
            if not self.BaseHasPylon(Base): return self.PylonSpotNearBase(Base)
            
        return self.PylonSpotNearBase(self.MainBase)
    
    async def GetSpotForGateway(self):
        #This function could definitely be better... 
        return self.PylonSpotNearBase(self.MainBase, Distance= 8)
    
    def PylonSpotNearBase(self, Base: Unit | Point2, Distance: int = 6) -> Point2:
        if Base:
            PatchesCentre = self.GetCentreOfBasePatches(Base)
            if PatchesCentre:
                return self.AwayFrom(Base, PatchesCentre, Distance)
    
    async def SimpleBuild(self, UnitID: int, Near: Point2 | Unit, CheckHaveEnoughSupply: bool = False) -> None:
        #We should be choosing a close by probe, we can improve this function if wanted
        await self.build(UnitID, near=Near)
        
    
    async def BuildPylons(self):
        if not self.NeedMorePylons:
            return 
        
        await self.SimpleBuild(UnitTypeId.PYLON, self.GetSpotForPylon())
    
    async def BuildGateways(self):
        if not self.NeedMoreGateways:
            return
        

        Location = await self.TimeIt(self.GetSpotForGateway, "GetSpotForGateway")
        if Location:
            self.CountTimesCalledPerPeriod("Build a gate")
            await self.SimpleBuild(UnitTypeId.GATEWAY, Location)
        
    async def Expand(self):
        if not self.NeedMoreExpansions:
            return
        
        Location = await self.get_next_expansion()
        if Location:
            self.CountTimesCalledPerPeriod("Expand")
            await self.SimpleBuild(UnitTypeId.NEXUS, Location)

            
    async def BuildCybercore(self):
        if not self.NeedCybercore:
            return
        
        Location = self.MainBase
        if Location:
            await self.SimpleBuild(UnitTypeId.CYBERNETICSCORE, Location)
        
    async def GetVespene(self):
        if not self.NeedVespeneBuildings: return
        
        TargetGeyser = self.NextGeyserToTake
        
        if not TargetGeyser: return

        await self.SimpleBuild(self.VespeneBuildingUnitTypeID, TargetGeyser)