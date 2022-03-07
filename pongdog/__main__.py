# -*- coding: utf-8 -*- 
from flask import Flask, request, render_template, Markup,flash,redirect,jsonify
import requests

app = Flask(__name__)
app.secret_key = "super secret key"
#CORS(app)
NUM_TABS = 3


@app.route("/")
def index():
    return redirect("/pongdog/lb_dynamic")

@app.route("/pongdog/register")
def register():
    return render_template("pongdog/registerpage.html")

@app.route("/pongdog/add_pong_dog",methods = ["POST"])
def add_pong_dog():
    card_no = request.form["card_id"]
    card_name = request.form["card_name"]
    
    card_id = reverseBytes(int(card_no))
    url = f"https://jakvah.pythonanywhere.com/add_new_pong_user/{card_id}/{card_name}"
    r = requests.post(url)
    
    if r.text == 200 or r.text == "200":
        flash_str = f"Successfully added {card_name}s card data!"
        flash(flash_str)
        return redirect("/pongdog/register")
    elif r.text == 300 or r.text == "300":
        flash_str = f"A card with that ID has already been registered!"
        flash(flash_str)
        return redirect("/pongdog/register")
    else:
        flash_str = f"Could not add {card_name}s card data!"
        flash(flash_str)
        return redirect("/pongdog/register")


@app.route("/pongdog/leaderboard")
def leaderboard():
    return render_template("pongdog/leaderboard.html")

@app.route("/pongdog/match_page")
def match_page():
    return render_template("pongdog/match_page.html")

@app.route("/dynamic_view")
def dynamic_view():
    pass

@app.route("/pongdog/match_page_2")

@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/pongdog/lb_dynamic")
def dynamic():
    return render_template("pongdog/lb_dynamic.html")

@app.route("/get_local_game_stat")
def get_local_scores():
    match_dict = {}
    
    lines = []
    with open('scores.txt') as f:
        lines = f.readlines()

    start_time = lines[0]
    p1_id = int(lines[1].split(",")[0])
    p1_name = lines[1].split(",")[1]        
    p1_elo = int(lines[1].split(",")[2])
    p1_score = int(lines[1].split(",")[3])

    p2_id = int(lines[2].split(",")[0])
    p2_name = lines[2].split(",")[1]
    p2_elo = int(lines[2].split(",")[2])
    p2_score = int(lines[2].split(",")[3])
    
    if (abs(p1_score -p2_score) >= 2) and (p1_score > 11 or p2_score > 11):
        ongoing = 0
    else:
        ongoing = 1
     
    if ongoing == 0:
        match_dict["ongoing"] = 0
        match_dict["start_time"] = "-"
        match_dict["player1_id"] = -1
        match_dict["player2_id"] = -1

        match_dict["player1_score"] = -1
        match_dict["player2_score"] = -1

        match_dict["player1_name"] = -1
        match_dict["player2_name"] = -1

        match_dict["player1_elo"] = -1
        match_dict["player2_elo"] = -1

        response = jsonify(match_dict)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        match_dict["ongoing"] = ongoing
        match_dict["start_time"] = start_time
        match_dict["player1_id"] = p1_id
        match_dict["player2_id"] = p2_id

        match_dict["player1_score"] = p1_score
        match_dict["player2_score"] = p2_score

        match_dict["player1_name"] = p1_name
        match_dict["player2_name"] = p2_name

        match_dict["player1_elo_win"] = elo_at_stake(p1_elo, p2_elo)[0]
        match_dict["player1_elo_loss"] = - \
            (elo_at_stake(p1_elo, p2_elo)[1])
        match_dict["player2_elo_win"] = elo_at_stake(p1_elo, p2_elo)[1]
        match_dict["player2_elo_loss"] = - \
            (elo_at_stake(p1_elo, p2_elo)[0])

        match_dict["player1_elo"] = p1_elo
        match_dict["player2_elo"] = p2_elo

        response = jsonify(match_dict)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response



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

if __name__ == '__main__':
    # Set debug false if it is ever to be deployed
    app.run(debug=True) 