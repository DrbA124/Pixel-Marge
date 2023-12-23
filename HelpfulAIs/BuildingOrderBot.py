from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit

import GeneralUtilsAI

class BuildingOrderBot(GeneralUtilsAI):
    def SelectBuildOrder(self):
        BuildOrderOptions = [
            """
            13	  0:18	  Pylon	  
            15	  0:37	  Gateway	  
            16	  0:48	  Assimilator	  
            19	  1:22	  Nexus	  
            21	  1:37	  Cybernetics Core	  
            21	  1:45	  Assimilator	  
            22	  1:51	  Pylon	  
            23	  2:15	  Adept, Warp Gate	  Scout with this
            26	  2:30	  Pylon	  
            27	  2:37	  Stargate
        """]
        
        print(BuildOrderOptions[0])