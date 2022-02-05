from multiprocessing import Condition
from utils import sound
from utils.cardreader import Cardreader
import time

sound.play_nice()
time.sleep(2)

class Player:
    def __init__(self,card_id, score):
        self.card_id = card_id
        self.score = score

    
#1. Poll Cards
#2. Start game
#3. Post score