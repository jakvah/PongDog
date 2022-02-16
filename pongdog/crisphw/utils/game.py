import math, time, random, pygame
from utils import sound

GAME_TIMEOUT = 600 #Game automatically stops after 600 seconds // 10 minutes

class Player:
    def __init__(self,card_id):
        self.card_id = card_id
        self.score = 0
        self.server = False
    
    def increment_score(self):
        self.score = self.score + 1

    def change_server(self):
        self.server = not self.server 
    

# main game logic
def start_game(p1, p2):
    start_time = time.time()
    player1, player2 = Player(p1), Player(p2)
    
    # ------- Window settings
    pygame.init()
    flags = pygame.FULLSCREEN
    screen = pygame.display.set_mode((1920,1080),flags)
    pygame.display.set_caption("PongDog")

    # ------- Text
    font = pygame.font.Font('freesansbold.ttf', 32)

    # ------- Game functions
    def show_score(x,y,score):
        score = font.render("Score: " + str(score), True, (0,0,0))
        screen.blit(score, (x, y))

    def draw_circle(x,y):
        circle = pygame.draw.circle(screen, (126,126,126),(x,y),200)

    # ------ Serve
    if random.randint(0,1) == 1:
        print("P1 serves")
        player1.server = True
    else:
        print("P2 serves")
        player2.server = True
    
    while True: #main game loop
        screen.fill((255,255,255))


        current_time = time.time()
        delta_time = round((current_time - start_time))
        if abs(player1.score-player2.score) >= 2 and (player1.score >= 11 or player2.score >= 11): # Game is won by normal means
            print("game over!")
            #send winners to database
            return
        if delta_time > GAME_TIMEOUT: # Game times out
            print("game timed out!")
            #return, do nothing
            return
        
        print("Round:" + str(player1.score + player2.score + 1))
        if (player1.score >= 10) and (player2.score >= 10):
            print("above 10: swapping servers")
            player1.change_server()
            player2.change_server()
            if player1.server:
                print("P1 is now serving")
            if player2.server:
                print("P2 is now serving")
        
        elif (player1.score + player2.score) % 2 == 0 and (player1.score + player2.score) > 0:
            print("swapping servers") 
            player1.change_server()
            player2.change_server()
            if player1.server:
                print("P1 is now serving")
            if player2.server:
                print("P2 is now serving")

        # if button_player1(ispressed):
            #player2.increment_score
            #roundcounter = roundcounter + 1

        # if button_player2(ispressed):
            #player2.increment_score()
            #round_counter = round_counter +1

        if random.randint(0,1) == 1:
            print("P1 scores!")
            player1.increment_score()
            sound.play_score_sound()
            
        else:
            print("P2 scores!")
            player2.increment_score()
            sound.play_score_sound()

        print("p1 score:" +  str(player1.score))
        print("p2 score:" +  str(player2.score))
        print("------")
        # ------- Update score, draw objects
        show_score(0,50,player1.score)
        show_score(650,50,player2.score)
        draw_circle(500,500)
        pygame.display.update()
        time.sleep(1)


def pygame_test():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("PongDog")
    font = pygame.font.Font('freesansbold.ttf', 64)

    def show_score(x,y):
        score = font.render("Score: " + str(20), True, (0,0,0))
        screen.blit(score, (x, y))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255,255,255))
        show_score(10,10)
        show_score(100,200)

        pygame.display.update()


if __name__ == "__main__":
    start_game(69,20)
    #pygame_test()