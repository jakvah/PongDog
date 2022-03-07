import math, time, random, pygame, os
from  utils.peripherals import post_winner
from utils import sound
from gpiozero import Button, LED

p1_led = LED(26)
p2_led = LED(16)
p1_button = Button(19)
p2_button = Button(20)


GAME_TIMEOUT = 600 #Game automatically stops after 600 seconds // 10 minutes

class Player:
    def __init__(self,card_id, name, elo):
        self.card_id = card_id
        self.name = name
        self.elo = elo
        self.score = 0
        self.server = False
        self.picture = False
        if os.path.isfile("images/profilepictures/"+str(self.card_id)+".png"):
            self.picture = True
            print(str(self.card_id)+ " has a profile picture.")
    
    def increment_score(self):
        self.score = self.score + 1

    def change_server(self):
        self.server = not self.server 

# props 2 Mathias Haugland
def elo_at_stake(p1_ELO,p2_ELO):
    adv = 1800 #if you have adv more points than your opponent you are 10 times more likely to win
    k = 50

    pow1 = ((p1_ELO-p2_ELO)/adv)
    exp_score1 = 1/(1+10**pow1)
    p1_win = k*exp_score1 #p1_win is what p1 wins and p2 looses

    pow2 = ((p2_ELO-p1_ELO)/adv)
    exp_score2 = 1/(1+10**pow2)
    p2_win = k*exp_score2 #p2_win is what p2 wins and p1 looses

    return str(round(p1_win)), str(round(p2_win))


# main game logic
def start_game(p1, p2, p1_name, p2_name, p1_elo, p2_elo):
    start_time = time.time()
    player1, player2 = Player(p1,p1_name,p1_elo), Player(p2,p2_name,p2_elo)

    p1_elo_gain, p2_elo_gain = elo_at_stake(player1.elo, player2.elo)
    
    # ------- Window settings
    pygame.init()
    flags = pygame.FULLSCREEN
    width = 1920   
    height = 1080
    screen = pygame.display.set_mode((0,0))
    pygame.display.set_caption("PongDog")

    # ------- Text and resources
    #font = pygame.font.Font('freesansbold.ttf', 64)
    scorefont = pygame.font.SysFont("Arial",64)
    namefont = pygame.font.SysFont("Arial",40)
    serveIndicator = pygame.image.load('images/serve.png')
    serveIndicator = pygame.transform.scale(serveIndicator,(100,100))
    bg = pygame.image.load('images/bg3.png')
    bg = pygame.transform.scale(bg, (width,height))

    #Profile Pictures
    if player1.picture:
        p1_pic = pygame.image.load('images/profilepictures/'+str(player1.card_id)+".png").convert_alpha()
        p1_pic = pygame.transform.scale(p1_pic, (300,300))

    if player2.picture:
        p2_pic = pygame.image.load('images/profilepictures/'+str(player2.card_id)+".png").convert_alpha()
        p2_pic = pygame.transform.scale(p2_pic, (300,300))
    # ------- Game functions
    def show_score(x,y,score):
        score = scorefont.render("Score: " + str(score), True, (0,0,0))
        screen.blit(score, (x, y))

    def draw_stats():
        p1_elo_text = scorefont.render("ELO: " + str(player1.elo),True, (0,0,0))
        p2_elo_text = scorefont.render("ELO: " + str(player2.elo),True, (0,0,0))
        p1_name_text = namefont.render(player1.name,True, (0,0,0))
        p2_name_text = namefont.render(player2.name,True, (0,0,0))
        elo_gain_text = namefont.render("Gain: ", True, (0,0,0))
        elo_loss_text = namefont.render("Loss: ", True, (0,0,0))
        p1_elo_gain_text = namefont.render(p1_elo_gain,True, (0,150,0))
        p1_elo_loss_text = namefont.render(p2_elo_gain,True, (150,0,0))
        p2_elo_gain_text = namefont.render(p2_elo_gain,True, (0,150,0))
        p2_elo_loss_text = namefont.render(p1_elo_gain,True, (150,0,0))
        screen.blit(p1_name_text, (width//6, height//1.85))
        screen.blit(p2_name_text, (width//1.525, height//1.85))
        screen.blit(elo_gain_text, (width//6, height//1.7))
        screen.blit(elo_gain_text, (width//1.525, height//1.7))
        screen.blit(p1_elo_gain_text, (width//4.7+20, height//1.7))
        screen.blit(p2_elo_gain_text, (width//1.425+20, height//1.7))
        screen.blit(elo_loss_text, (width//6, height//1.58))
        screen.blit(elo_loss_text, (width//1.525, height//1.58))
        screen.blit(p1_elo_loss_text, (width//4.7+20, height//1.58))
        screen.blit(p2_elo_loss_text, (width//1.425+20, height//1.58))
        screen.blit(p1_elo_text, (width//6, height//2.10))
        screen.blit(p2_elo_text, (width//1.525, height//2.10))

    def draw_timer(timevalue):
        formattedtime = time.strftime('%M:%S', time.gmtime(timevalue))
        timestamp = scorefont.render(formattedtime, True, (74, 111, 125))
        screen.blit(timestamp, (width/2-85,60))

    def draw_profile_pictures():
        if player1.picture:
            screen.blit(p1_pic,(width//5.7,height//5.14))
        if player2.picture:
            screen.blit(p2_pic,(width//1.51, height//5.14))
    def draw_circle(x,y, radius,color):
        circle = pygame.draw.circle(screen, color,(x,y),radius)

    def draw_serve_indicator(p1_server):
        if p1_server:
            screen.blit(serveIndicator,(width//3.95,110))
        else:
            screen.blit(serveIndicator,(width//1.35,110))

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
        #draw_circle(width//2-15,130,100,(200,200,200))
        draw_timer(delta_time)
        if abs(player1.score-player2.score) >= 2 and (player1.score >= 11 or player2.score >= 11): # Game is won by normal means
            print("game over!")
            draw_profile_pictures()
            show_score(width//5.32,height/1.4,player1.score)
            show_score(width//1.48,height/1.4,player2.score)
            draw_stats()
            draw_serve_indicator(player1.server)
            pygame.display.update()
            sound.play_game_over()
            if player1.score > player2.score:
                post_winner(player1.card_id,player2.card_id)
                print(player1.name +" won!")
            else:
                post_winner(player2.card_id,player1.card_id)
                print(player2.name +" won!")
            time.sleep(5)
            pygame.display.quit()
            #send winners to database
            return
        if delta_time > GAME_TIMEOUT: # Game times out
            print("game timed out!")
            #return, do nothing
            return

         # ------- Update score, draw objects
        #draw_circle(width//3.95,height//3,150,(52, 225, 235))
        #draw_circle(width//1.35,height//3,150,(52, 225, 235))
        draw_profile_pictures()
        show_score(width//5.32,height/1.4,player1.score)
        show_score(width//1.48,height/1.4,player2.score)
        draw_stats()
        draw_serve_indicator(player1.server)


        p1_button.when_pressed = increment_score_p1
        p2_button.when_pressed = increment_score_p2
        
        # -- update screen
        pygame.display.update()


if __name__ == "__main__":
    start_game(69,20)
    #pygame_test()