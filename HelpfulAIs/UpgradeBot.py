from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2
from sc2.unit import Unit
from sc2.ids.upgrade_id import UpgradeId

from HelpfulAIs.ProtossUtilsAI import ProtossUtilsAI


class UpgradeBot(ProtossUtilsAI):
    def NeedsAndCanGetUpgrade(self, ID: UpgradeId, Building: UnitTypeId = "Irrelevant", Prerequisite: UnitTypeId | UpgradeId = "Irrelevant") -> bool:
        if Building != "Irrelevant" and Prerequisite != "Irrelevant":
            return self.can_afford(ID) and self.Has(Building) and self.HasUpgrade(Prerequisite) and not self.already_pending_upgrade(ID)
        
        if Building != "Irrelevant":
            return self.can_afford(ID) and self.Has(Building) and not self.already_pending_upgrade(ID)
        
        if Prerequisite != "Irrelevant":
            return self.can_afford(ID) and self.HasUpgrade(Prerequisite) and not self.already_pending_upgrade(ID)
        
        else:
            return self.can_afford(ID) and not self.already_pending_upgrade(ID)
            
    def HasUpgrade(self, Id):
        return Id in self.state.upgrades
    
    async def GetWarpGate(self) -> None:
        ID = UpgradeId.WARPGATERESEARCH
        if self.NeedsAndCanGetUpgrade(ID, UnitTypeId.CYBERNETICSCORE):
            self.research(ID)
            
            
    
    async def GetUpgrades(self):
        await self.GetWarpGate()