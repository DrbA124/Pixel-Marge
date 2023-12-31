from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sc2.position import Point2

from HelpfulAIs.GeneralUtilsAI import GeneralUtilsAI

class BuildingBot(GeneralUtilsAI):
    async def BuildUnit(self, DemandedUnit: UnitTypeId) -> None: # This will be called by the BuildOrderBot when it wants a certain unit (including structures)
        
        await self.build(DemandedUnit, self.MainBase) # This is temporary and should be replaced!
        #Plan is to have "if the demanded unit's a pylon, do this, if it's a gate, do that, if it's a stargate etc etc"
        
    
    def FindPylonLocations(self, Base: Unit | Point2, Distance: int = 6):
        if self.Bases:
            for Base in self.Bases:
                PatchesCentre = self.GetCentreOfBasePatches(Base)
                if PatchesCentre:
                    return self.AwayFrom(Base, PatchesCentre, Distance)

    async def BuildFirstPylon(self):
        if (
            self.supply_workers == 15 and
            self.can_afford(UnitTypeId.PYLON) and
            self.structures(UnitTypeId.PYLON).amount == 0
        ):
            await self.build(UnitTypeId.PYLON, self.MainBase) #added some temp code here so I can finish some of my stuff - Dom
        elif (
            None
        ):
            pass