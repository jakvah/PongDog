from multiprocessing import Condition
from utils import sound
import time

while(True):
    sound.play_score_sound()
    time.sleep(0.5)