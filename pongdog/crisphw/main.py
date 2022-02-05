from multiprocessing import Condition
from utils import sound
from utils.cardreader import Cardreader
import time

sound.play_nice()
time.sleep(2)
while(True):
    sound.play_score_sound()
    time.sleep(0.5)
    #Cardreader.run()


#1. Poll Cards
#2. Start game
#3. Post score