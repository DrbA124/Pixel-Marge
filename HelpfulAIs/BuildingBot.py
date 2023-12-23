from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sc2.position import Point2

from HelpfulAIs.GeneralUtilsAI import GeneralUtilsAI

#Make Pylons
class BuildingBot(GeneralUtilsAI):
    def FindPylonLocations(self, Base: Unit | Point2, Distance: int = 6):
        if self.Bases:
            for Base in self.Bases:
                PatchesCentre = self.GetCentreOfBasePatches(Base)
                if PatchesCentre:
                    return self.AwayFrom(Base, PatchesCentre, Distance)

    def BuildFirstPylon(self):
        if (
            self.supply_workers == 15 and
            self.can_afford(UnitTypeId.PYLON) and
            self.structures(UnitTypeId.PYLON).amount == 0
        ):
            await self.build(UnitTypeId.PYLON, location)
        elif (

        ):
