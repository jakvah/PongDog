import math, time, random

class Player:
    def __init__(self,card_id):
        self.card_id = card_id
        self.score = 0
    
    def increment_score(self):
        self.score = self.score + 1
        print(self.score)
    
def start_game(p1, p2):
    player1, player2 = Player(p1), Player(p2)
    player2.score = 2
    while True:
        if abs(player1.score-player2.score) >= 2 and (player1.score >= 11 or player2.score >= 11):
            print("game over!")
            return
        player1.increment_score()
        player2.increment_score()
        print(abs(player1.score - player2.score))
if __name__ == "__main__":
    start_game(69,20)