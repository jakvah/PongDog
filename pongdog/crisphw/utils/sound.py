import pygame,random

print("Initializing sound mixer")
pygame.mixer.init()
assert(pygame.mixer.get_init())
nice = pygame.mixer.Sound(file="sound/nice.ogg")
boom = pygame.mixer.Sound(file="sound/boom.ogg")
coin = pygame.mixer.Sound(file="sound/coin.ogg")
game = pygame.mixer.Sound(file="sound/game.ogg")
mja  = pygame.mixer.Sound(file="sound/nja.ogg")
playerregistered = pygame.mixer.Sound(file="sound/playerregistered.ogg")
gamestart = pygame.mixer.Sound(file="sound/gamestart.ogg")
coin.set_volume(0.3)

# Plays "boom" or mario coin when you take a point
def play_score_sound():
    if random.randint(0,100) < 5: # 5% chance for the boom playing
        boom.play()
    else:
        coin.play()    
# Says "Game!"
def play_game_over():
    game.play()
    
def play_mja():
    mja.play()

# Sound that plays when card is registered
def play_player_registered():
    playerregistered.play

# Plays a sound when the game is about to start.
def play_game_start():
    gamestart.play()

# *Click* Nice!
def play_nice():
    nice.play()



