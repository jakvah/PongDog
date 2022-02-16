from multiprocessing import Condition
from utils import sound, game
from utils.cardreader import Cardreader
import time, random

random.seed()

game.start_game(100,102)
#1. Poll Cards
#2. Start game
#3. Post score