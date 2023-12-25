from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.unit import Unit

from HelpfulAIs.GeneralUtilsAI import GeneralUtilsAI

class UpgradeBot(GeneralUtilsAI):
    async def GetUpgrade(self, DemandedUpgrade: UpgradeId) -> None: # This will be called by the BuildOrderBot when it wants a certain upgrade
        pass