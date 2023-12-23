from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer

from HelpfulAIs import TrainingBot

'''
TODO:
Find depowered buildings and repower. prioritise over building other pylons

'''

class PixelMargeBot(TrainingBot):
    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send("GG EZ")
        
        #await self.ControlWorkers()
        await self.TimeIt(self.distribute_workers, "distribute_workers")
        
            
        self.GetDebugInfo(True, Iteration = iteration)
        
        await self.TimeIt(self.PrepareForNextStep, "PrepForNext") 

 


def main():
    run_game(
        maps.get("AbyssalReefLE"),
        [Bot(Race.Protoss, PixelMargeBot(), name="PixelMarge"),
         Computer(Race.Protoss, Difficulty.Easy)],
        realtime=True,
    )


if __name__ == "__main__":
    main()