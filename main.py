import sc2
import random
from sc2.data import Race, Difficulty
from sc2.main import run_game
from sc2.player import Bot, Human, Computer
from sc2 import maps
from PixelMarge import PixelMargeBot

bot = Bot(Race.Terran, ())
human = Human(Race.Zerg, fullscreen=True)
ai = Computer(Race.Zerg, Difficulty.VeryHard)

#Adding comment! And me too!

def main():
    mapit = [
        "AcropolisLE",
    ]
    map_name = random.choice(mapit)

    run_game(
        maps.get(map_name),
        [bot, ai],
        realtime=False
    )


if __name__ == '__main__':
    main()
