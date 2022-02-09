import math, time, random

GAME_TIMEOUT = 600 #Game automatically stops after 600 seconds // 10 minutes

class Player:
    def __init__(self,card_id):
        self.card_id = card_id
        self.score = 0
        self.server = False
    
    def increment_score(self):
        self.score = self.score + 1
        print(self.score)
    
def start_game(p1, p2):
    if random.randint(0,1) == 1:
        print("P1 serves")
    else:
        print("P2 serves")
    starttime = time.time()
    player1, player2 = Player(p1), Player(p2)
    player2.score = 2
    while True:
        currenttime = time.time()
        deltatime = round((currenttime - starttime))
        if abs(player1.score-player2.score) >= 2 and (player1.score >= 11 or player2.score >= 11): # Game is won by normal means
            print("game over!")
            return
        if deltatime > GAME_TIMEOUT: # Game times out
            print("game timed out!")
            return
        player1.increment_score()
        player2.increment_score()
        time.sleep(0.2)
if __name__ == "__main__":
    start_game(69,20)
    start_game(40,23)