from multiprocessing import Condition
from utils import sound, game, peripherals
from utils.cardreader import Cardreader
import time, random

random.seed()


#Player1 = Cardreader.run()
#print(Player1)
p1_card = 317094323
p1_name, p1_elo = peripherals.get_name_and_elo(p1_card)
p2_card = 128
p2_name, p2_elo = peripherals.get_name_and_elo(p2_card)
peripherals.fetch_player_image(p1_card)
peripherals.fetch_player_image(p2_card)
#peripherals.convert_image_to_png("2")
game.start_game(p1_card,p2_card,p1_name,p2_name,p1_elo,p2_elo)
#1. Poll Cards
#2. Start game
#3. Post score