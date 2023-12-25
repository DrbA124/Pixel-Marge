from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer

from HelpfulAIs.TrainingBot import TrainingBot
from HelpfulAIs.BuildingOrderBot import BuildingOrderBot
from HelpfulAIs.BuildingBot import BuildingBot


class PixelMargeBot(TrainingBot, BuildingOrderBot, BuildingBot):
    async def on_step(self, iteration):
        if iteration == 0:
            self.IsFirstStep = True
            await self.chat_send("GG EZ")
        else: self.IsFirstStep = False
        
        #await self.ControlWorkers()
        await self.TimeIt(self.distribute_workers, "distribute_workers")
        await self.TimeIt(self.TrainWorkers, "TrainWorkers")
        await self.TimeIt(self.ExecuteBuildOrder, "ExecuteBuildOrder")
            
        self.GetDebugInfo(True, Iteration = iteration)
        
        await self.TimeIt(self.PrepareForNextStep, "PrepForNext") 

 