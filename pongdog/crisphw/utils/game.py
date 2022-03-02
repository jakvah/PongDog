import math, time, random, pygame
from utils import sound
from gpiozero import Button, LED

p1_led = LED(26)
p2_led = LED(16)
p1_button = Button(19)
p2_button = Button(20)


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
    width = 1920   
    height = 1080
    screen = pygame.display.set_mode((0,0), flags)
    pygame.display.set_caption("PongDog")

    # ------- Text and resources
    font = pygame.font.Font('freesansbold.ttf', 64)
    serveIndicator = pygame.image.load('images/serve.png')
    serveIndicator = pygame.transform.scale(serveIndicator,(100,100))
    bg = pygame.image.load('images/bg2.jpg')
    bg = pygame.transform.scale(bg, (width,height))
    # ------- Game functions
    def show_score(x,y,score):
        score = font.render("Score: " + str(score), True, (0,0,0))
        screen.blit(score, (x, y))
    
    def draw_timer(timevalue):
        formattedtime = time.strftime('%M:%S', time.gmtime(timevalue))
        timestamp = font.render(formattedtime, True, (57, 71, 54))
        screen.blit(timestamp, (width/2-100,100))

    def draw_circle(x,y, radius,color):
        circle = pygame.draw.circle(screen, color,(x,y),radius)

    def draw_serve_indicator(p1_server):
        if p1_server:
            screen.blit(serveIndicator,(500-20,200))
        else:
            screen.blit(serveIndicator,(1400-20,200))

    def draw_background():
        screen.blit(bg,(0,0))

    def increment_score_p1():
        sound.play_score_sound()
        player1.increment_score()
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
        #roundcounter = roundcounter + 1
        time.sleep(0.5)

    def increment_score_p2():
        sound.play_score_sound()
        player2.increment_score()
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
        #roundcounter = roundcounter + 1
        time.sleep(0.5)
        

    # ------ Serve
    if random.randint(0,1) == 1:
        print("P1 serves")
        player1.server = True
    else:
        print("P2 serves")
        player2.server = True
    
    while True: #main game loop
        screen.fill((255,255,255))
        draw_background()
        current_time = time.time()
        delta_time = round((current_time - start_time))
        draw_circle(width//2-15,130,100,(200,200,200))
        draw_timer(delta_time)
        if abs(player1.score-player2.score) >= 2 and (player1.score >= 11 or player2.score >= 11): # Game is won by normal means
            print("game over!")
            sound.play_game_over()
            time.sleep(5)
            #send winners to database
            return
        if delta_time > GAME_TIMEOUT: # Game times out
            print("game timed out!")
            #return, do nothing
            return

         # ------- Update score, draw objects
        draw_circle(500,500,200,(52, 225, 235))
        draw_circle(1420,500,200,(52, 225, 235))
        show_score(500-120,700,player1.score)
        show_score(width-500-120,700,player2.score)
        draw_serve_indicator(player1.server)


        p1_button.when_pressed = increment_score_p1
        p2_button.when_pressed = increment_score_p2
        
        # -- update screen
        pygame.display.update()


def pygame_test():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("PongDog")
    font = pygame.font.Font('RobotoSlab-Bold.ttf', 64)

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