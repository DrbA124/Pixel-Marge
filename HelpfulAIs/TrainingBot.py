from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit

from HelpfulAIs.ProtossUtilsAI import ProtossUtilsAI

class TrainingBot(ProtossUtilsAI):
    @property
    def WorkerCount(self):
        BuildingWorkers = 0
        return self.supply_workers + BuildingWorkers
    
    @property
    def NeedMoreWorkers(self):
        return self.WorkerCount < 80
    
    
    async def TrainWhenCan(self, TrainerID, UnitID):
        PotentialTrainers = self.all_own_units(TrainerID)
        ReadyPotentialTrainers = PotentialTrainers.filter(lambda structure: structure.is_ready and structure.is_idle)
        
        if ReadyPotentialTrainers:
             Trainer = ReadyPotentialTrainers.first
        else: return 

        if self.can_afford(UnitID) and self.can_feed(UnitID) and Trainer:    
            Trainer.train(UnitID)
    
    async def TrainWorkers(self):
        if not self.NeedMoreWorkers:
            return
        
        if self.townhalls.exists:
            await self.TrainWhenCan(UnitTypeId.NEXUS, UnitTypeId.PROBE)
        
            