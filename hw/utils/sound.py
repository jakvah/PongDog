import pygame,random, os, time
print("Initializing sound mixer")
random.seed()

pygame.mixer.init()
pygame.init()
print("Sound mixer initialized")
nice = pygame.mixer.Sound(file="/home/pi/PongDog/hw/sound/nice.ogg")
boom = pygame.mixer.Sound(file="/home/pi/PongDog/hw/sound/boom.ogg")
coin = pygame.mixer.Sound(file="/home/pi/PongDog/hw/sound/coin.ogg")
game = pygame.mixer.Sound(file="/home/pi/PongDog/hw/sound/game.ogg")
playerregistered = pygame.mixer.Sound(file="/home/pi/PongDog/hw/sound/playerregistered.ogg")
gamestart = pygame.mixer.Sound(file="/home/pi/PongDog/hw/sound/gamestart.ogg")
nja = pygame.mixer.Sound(file="/home/pi/PongDog/hw/sound/nja.wav")
coin.set_volume(0.3)

# Plays "boom" or mario coin when you take a point
def play_score_sound():
    randomvar = random.randint(0,100)
    if randomvar < 5 and randomvar > 1: # 5% chance for the boom playing
        boom.play()
    elif randomvar == 1: # 1% chance for at bomben sier nja
        nja.play()
    else:
        coin.play()    
# Says "Game!"
def play_game_over():
    game.play()

# Sound that plays when card is registered
def play_player_registered():
    playerregistered.play

# Plays a sound when the game is about to start.
def play_game_start():
    gamestart.play()

# *Click* Nice!
def play_nice():
    nice.play()

def bomben_synger():
    pygame.mixer.music.load("/home/pi/PongDog/hw/sound/bombengoinghard.mp3")
    pygame.mixer.music.play()

def bomben_holder_kjeft():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

def play_nja():
    nja.play()
