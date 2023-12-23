from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer

from HelpfulAIs.TrainingBot import TrainingBot
from HelpfulAIs.BuildingBot import BuildingBot
from HelpfulAIs.UpgradeBot import UpgradeBot

'''
TODO:
Cybercore.
Find depowered buildings and repower. prioritise over building other pylons

'''

class MargeBot(TrainingBot, BuildingBot, UpgradeBot):
    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send("GG EZ")
        
        #await self.ControlWorkers()
        await self.TimeIt(self.TrainWorkers, "TrainWorkers")
        await self.TimeIt(self.distribute_workers, "distribute_workers")
        await self.TimeIt(self.BuildPylons, "BuildPylons")
        await self.TimeIt(self.BuildGateways, "BuildGateways")
        await self.TimeIt(self.Expand, "Expand")
        await self.TimeIt(self.BuildCybercore, "BuildCybercore")
        await self.TimeIt(self.GetUpgrades, "GetUpgrades")
        await self.TimeIt(self.GetVespene, "GetVespene")
        

            
        self.GetDebugInfo(True, Iteration = iteration)
        
        await self.TimeIt(self.PrepareForNextStep, "PrepForNext") 


    
    
        


def main():
    run_game(
        maps.get("AbyssalReefLE"),
        [Bot(Race.Protoss, MargeBot(), name="Marge"),
         Computer(Race.Protoss, Difficulty.Easy)],
        realtime=True,
    )


if __name__ == "__main__":
    main()