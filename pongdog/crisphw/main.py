from multiprocessing import Condition
from utils import sound, game, peripherals
from utils.cardreader import Cardreader
import time, random

random.seed()

#peripherals.fetch_player_image(317094323)
game.start_game(100,102)
#1. Poll Cards
#2. Start game
#3. Post score