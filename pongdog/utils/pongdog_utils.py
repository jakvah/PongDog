"""
PongDog Utils
"""
# FROM: https://github.com/hermabe/rfid-card
# Reverses CARD EM number to RFID number
def reverseBytes(number):
    binary = "{0:0>32b}".format(number) # Zero-padded 32-bit binary
    byteList = [binary[i:i+8][::-1] for i in range(0, 32, 8)] # Reverse each byte
    return int(''.join(byteList), 2) # Join and convert to decimal
    # return int(''.join(["{0:0>32b}".format(number)[i:i+8][::-1] for i in range(0, 32, 8)]), 2)

def elo_at_stake(p1_ELO, p2_ELO):
    adv = 1800  # if you have adv more points than your opponent you are 10 times more likely to win
    k = 50

    pow1 = ((p1_ELO-p2_ELO)/adv)
    exp_score1 = 1/(1+10**pow1)
    p1_win = k*exp_score1  # p1_win is what p1 wins and p2 looses

    pow2 = ((p2_ELO-p1_ELO)/adv)
    exp_score2 = 1/(1+10**pow2)
    p2_win = k*exp_score2  # p2_win is what p2 wins and p1 looses

    return round(p1_win), round(p2_win)


def new_scores(p1_ELO, p2_ELO, winner):  # winner is 'p1' or 'p2'
    p1_win, p2_win = elo_at_stake(p1_ELO, p2_ELO)
    if winner == 'p1':
        p1_ELO_new = p1_ELO + p1_win
        p2_ELO_new = p2_ELO - p1_win
    elif winner == 'p2':
        p1_ELO_new = p1_ELO - p2_win
        p2_ELO_new = p2_ELO + p2_win
    else:
        print("Theres a bloody problem here, wankers, arrrrrghhh")

    if p1_ELO_new <= 0:
        p1_ELO_new = 0

    if p2_ELO_new <= 0:
        p2_ELO_new = 0

    return p1_ELO_new, p2_ELO_new
