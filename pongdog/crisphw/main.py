from multiprocessing import Condition
from utils import sound
from utils.cardreader import Cardreader
import time

while(True):
    sound.play_score_sound()
    time.sleep(0.5)
    Cardreader.run()