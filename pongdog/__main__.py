# -*- coding: utf-8 -*- 
from flask import Flask, request, render_template, Markup,flash,redirect,jsonify, g
import requests
import mysql.connector

from pongdog.config import pongdog_config as pc
from pongdog.api import local_db as ldb
from pongdog.utils import pongdog_utils as pu
from pongdog.utils import backend_utils as bu

TEST = True

app = Flask(__name__)
app.secret_key = "super secret key"
#CORS(app)
NUM_TABS = 3

def get_conn():

    if not hasattr(g, 'db_conn'):
        if pc.DOCKER:
            g.db_conn = mysql.connector.connect(host = 'gamedb', user = 'root', password = 'root', database = "game_db", port = 3306)
        else:
            g.db_conn = ldb.get_database_connection(pc.DOCKER)
    return g.db_conn



@app.route("/")
def index():
    return redirect("/pongdog/lb_dynamic")

@app.route("/knapper")
def knapp():
    return render_template("pongdog/knapp.html")

@app.route("/pongdog/leaderboard")
def leaderboard():
    return render_template("pongdog/leaderboard.html")

@app.route("/pongdog/match_page")
def match_page():
    return render_template("pongdog/match_page.html")

@app.route("/pongdog/lb_dynamic")
def dynamic():
    return render_template("pongdog/lb_dynamic.html")

@app.route("/pongdog/register")
def register():
    return render_template("pongdog/registerpage.html")


@app.route("/init_game/<p1_id>/<p2_id>/<time_stamp>",methods = ["POST"])
def init_game(p1_id,p2_id,time_stamp):
    CONN = get_conn()
    CUR = CONN.cursor()
    if ldb.is_match_ongoing(CONN,CUR):
        if TEST:
            flash("Executed request with response: 300")
            return redirect("/knapper")
        else:
            return "300"
    
    p1_elo, p1_name = bu.get_player_overview(p1_id)
    p2_elo,p2_name = bu.get_player_overview(p2_id)
    
    try:
        ldb.init_match(CONN,CUR, p1_id,p2_id,p1_elo,p2_elo,p1_name,p2_name,time_stamp)
        if TEST:
            flash(f"Executed request with response: 200")
            return redirect("/knapper")
        return "200"
    except Exception as e:
        return "400"

@app.route("/increment_score/<player_num>",methods = ["POST"])
def increment_score(player_num):
    if player_num != "p1" and player_num != "p2": raise ValueError(f"Invalid indentifier:{player_num}")
    
    try:
        CONN = get_conn()
        CUR = CONN.cursor()
        # Check if match is ongoing
        if not ldb.is_match_ongoing(CONN,CUR):
            if TEST:
                flash("Executed requeset with response: 300")
                return redirect("/knapper")
            else:
                return "300"
        ldb.increment_score(CONN,CUR, player_num)

        game_stat = ldb.get_local_game_state(CONN,CUR)
        p1_id = game_stat[1]
        p2_id = game_stat[2]
        p1_score = game_stat[7]
        p2_score = game_stat[8]
        
        diff = abs(p1_score - p2_score)
        if (p1_score >= 11 and diff >= 2) or (p2_score >= 11 and diff >= 2):
            ldb.limbo_match(CONN,CUR)
            bu.add_result(p1_id,p2_id,p1_score,p2_score)
            
        if TEST:
            flash(f"Executed request with response: 200")
            return redirect("/knapper")
        return "200"
    except Exception as e:
        return str(e)



@app.route("/pongdog/add_pong_dog",methods = ["POST"])
def add_pong_dog():
    card_no = request.form["card_id"]
    card_name = request.form["card_name"]
    
    card_id = pu.reverseBytes(int(card_no))
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


@app.route("/get_local_game_stat")
def get_local_scores():
    CONN = get_conn()
    CUR = CONN.cursor()
    match_dict = {}
    table = ldb.get_local_game_state(CONN,CUR)
    
    ongoing = table[0]
    p1_id = table[1]
    p2_id = table[2]
    p1_elo = table[3]
    p2_elo = table[4]
    p1_name = table[5]
    p2_name = table[6]
    p1_score = table[7]
    p2_score = table[8]
    start_time = table[9]
    

    if (abs(p1_score -p2_score) >= 2) and (p1_score >= 11 or p2_score >= 11):
        ongoing = 2
    elif p1_score == -1 and p2_score == -1:
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

        match_dict["player1_elo_win"] = pu.elo_at_stake(p1_elo, p2_elo)[0]
        match_dict["player1_elo_loss"] = - \
            (pu.elo_at_stake(p1_elo, p2_elo)[1])
        match_dict["player2_elo_win"] = pu.elo_at_stake(p1_elo, p2_elo)[1]
        match_dict["player2_elo_loss"] = - \
            (pu.elo_at_stake(p1_elo, p2_elo)[0])

        match_dict["player1_elo"] = p1_elo
        match_dict["player2_elo"] = p2_elo

        response = jsonify(match_dict)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


@app.route("/reset_match_status/pongdg4life", methods = ["POST"])
def reset_mach():
    try:
        CONN = get_conn()
        CUR = CONN.cursor()
        ldb.reset_match(CONN,CUR)
        if TEST:
            flash(f"Executed request with response: 200")
            return redirect("/knapper")
        return "200"
    except Exception as e:
        return "400"


if __name__ == '__main__':
    print("Initializing database...")
    #CONN = get_conn()
    #CUR = CONN.cursor()
    ldb.setup(docker=pc.DOCKER)

    # Set debug false if it is ever to be deployed
    print("Starting game server ...")
    app.run(debug=True, host="0.0.0.0") 