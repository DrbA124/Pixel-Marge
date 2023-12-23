from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sc2.position import Point2

from HelpfulAIs.GeneralUtilsAI import GeneralUtilsAI

class ProtossUtilsAI(GeneralUtilsAI):
    def PylonsNearUnit(self, Position: Point2 | Unit, Distance: int = 10):
        return self.units.closer_than(Distance, Position).filter(lambda Unit: Unit.type_id == UnitTypeId.PYLON)
    
    def BaseHasPylon(self, Base):
        return bool(self.PylonsNearUnit(Base, 15))