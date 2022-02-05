import pygame,random, time

print("Initializing sound mixer")
random.seed()
pygame.mixer.init()
assert(pygame.mixer.get_init())
boom = pygame.mixer.Sound(file="sound/boom.mp3")
coin = pygame.mixer.Sound(file="sound/coin.mp3")
game = pygame.mixer.Sound(file="sound/game.mp3")
playerregistered = pygame.mixer.Sound(file="sound/playerregistered.mp3")
gamestart = pygame.mixer.Sound(file="sound/gamestart.mp3")
playerregistered.play()
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

# Sound that plays when card is registered
def play_player_registered():
    playerregistered.play

def play_game_start():
    gamestart.play()



