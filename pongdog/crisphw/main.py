from multiprocessing import Condition
from utils import sound, game, peripherals
from utils.cardreader import Cardreader
import pygame
import time, random

random.seed()


while True:
    pygame.init()
    while True:
        game.blink_p1_led(1,1,10)
        game.blink_p2_led(1,1,10)
        print("Player 1, please scan card:")
        p1_card = Cardreader.run()
        if p1_card == "0":
            print("No card detected")
            continue
        print(p1_card)
        sound.play_mja()
        print("Player 2, please scan card:")
        p2_card = Cardreader.run()
        if p2_card == p1_card:
            print("Player already registered")
            continue
        if p2_card != p1_card and p2_card != "0":
            break
    print(p2_card)
    sound.play_mja()
    #print(Player1)
    #p1_card = 317094323
    p1_name, p1_elo = peripherals.get_name_and_elo(p1_card)
    p2_name, p2_elo = peripherals.get_name_and_elo(p2_card)
    print(p2_name)
    if p1_name == 0 or p2_name == 0:
        print("One of the players has not registered.")
        continue
    peripherals.fetch_player_image(p1_card)
    peripherals.fetch_player_image(p2_card)
    #peripherals.convert_image_to_png("2")
    game.start_game(p1_card,p2_card,p1_name,p2_name,p1_elo,p2_elo)
    p1_card = 0
    p2_card = 0
    pygame.quit()
    #1. Poll Cards
    #2. Start game
    #3. Post score