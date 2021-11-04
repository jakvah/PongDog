from flask import Flask, jsonify,flash,redirect,request,render_template
import db_manager as dbm
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = '/home/jakvah/mysite/user_imgs'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.secret_key = "super secret key"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
General API response codes for DogAPI:
    - 200: Success.
    - 300: The thing you are trying to do/add has already been done/added.
    - 400: Failed.
"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/add_new_pong_user",methods=["GET","POST"])
def test():
    try:
        if request.method == "GET":
            return "get in"
        if request.method == 'POST':
            # Handle card
            card_no = request.form["card_id"]
            card_name = request.form["card_name"]

            card_id = reverseBytes(int(card_no))
            if not dbm.pong_user_exists(card_id,table_name = "pongdog_users"):
                dbm.add_pong_dog_user(card_id,card_name)

                # Handle image
                if 'file' not in request.files:
                    flash(f'Successfully added {card_name}s card data!')
                    return render_template("registerpage.html")
                file = request.files['file']
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                if file.filename == '':
                    flash(f'Successfully added {card_name}s card data, but an invalid image file was attached, thus no image has been added!')
                    return render_template("registerpage.html")
                if file and allowed_file(file.filename):
                    filename = secure_filename(str(card_id))
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash(f"Successfully added {card_name}s card data and image!")
                    return render_template("registerpage.html")
            else:
                # Handle image
                if 'file' not in request.files:
                    flash('A card with that ID has already been registered!')
                    return render_template("registerpage.html")
                file = request.files['file']
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                if file.filename == '':
                    flash('A card with that ID has already been registered!')
                    return render_template("registerpage.html")
                if file and allowed_file(file.filename):
                    filename = secure_filename(str(card_id))
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash("A card with that ID has already been registered, but the image has been updated!")


                    return render_template("registerpage.html")
    except Exception as e:
        s = str(e)
        return s


@app.route("/get_card_status/<card_id>")
def get_card_status(card_id):
    try:
        if dbm.pong_user_exists(int(card_id)):
            return "200" # User exists
        else:
            return "300" # User not reg
    except Exception:
        return "400" # ERROR

@app.route("/get_match_status")
def get_match_status():
    try:
        if dbm.is_match_ongoing():
            return "200" # ongoing
        else:
            return "300" # available match
    except Exception:
        return "400" # ERROR

# Start time has format yyyy-mm-ddThh:mm:ss
# I.e 2021-04-01T07:00:00
@app.route("/init_match/<p1_id>/<p2_id>/<start_time>",methods = ["GET","POST"])
def init_match(p1_id,p2_id,start_time):
    try:
        if request.method == "GET":
            return "No access this way!"

        # POST method
        else:
            if dbm.is_match_ongoing():
                return "300" # Ongoing
            else:
                if dbm.init_match(p1_id,p2_id,start_time):
                    return "200"
                else:
                    return "400"
    except Exception:
        return "400"

@app.route("/reset_match_status/<pwd>")
def reset_match_status(pwd):
    if pwd == "pongdg4life":
        dbm.reset_match_status()
        res = "200"
    else:
        res = "300"

    response = jsonify(res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/increment_score/<player_num>")
def increment_score(player_num):
    if not int(player_num) in [1,2]:
        return "300" # Invalid player num (not 1 or 2)
    else:
        if not dbm.is_match_ongoing():
            return "300"
        if dbm.increment_score(int(player_num)):
            match_row = dbm.get_match_stats()
            p1_id = match_row[1]
            p2_id = match_row[2]
            player1_score = match_row[3]
            player2_score = match_row[4]
            start_time = match_row[5]
            diff = abs(player1_score - player2_score)
            if (player1_score >= 11 and diff >= 2) or (player2_score >= 11 and diff >= 2):
                if dbm.limbo_match(p1_id,p2_id,player1_score,player2_score,start_time):
                    return "300" # Set match in limbo state
                else:
                    return "400" # Error

            else:
                return "200" # Success
        else:
            return "400" # Error



@app.route("/get_pongdog_leaderboard",methods = ["GET"])
def get_pongdog_leaderboard():
    dataset = dbm.get_sorted_pongdog_leaderboard()
    scores_list = []

    for i,row in enumerate(dataset):
        score_dict = {}

        score_dict["name"] = row[2]
        score_dict["id"] = row[1]
        score_dict["score"] = row[3]
        score_dict["rank"] = i+1
        scores_list.append(score_dict)
    obj = {"scores" : scores_list}
    response = jsonify(obj)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/get_complete_match_stats")
def get_complete_match_stats():
    match_dict = {}
    match_row = dbm.get_match_stats()
    ongoing = match_row[0]

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


    player1_id = match_row[1]
    player2_id = match_row[2]
    player1_score = match_row[3]
    player2_score = match_row[4]
    start_time = match_row[5]

    player1_name = dbm.get_player_name(player1_id)
    player2_name = dbm.get_player_name(player2_id)
    player1_elo = dbm.get_player_elo(player1_id)
    player2_elo = dbm.get_player_elo(player2_id)

    match_dict["ongoing"] = ongoing
    match_dict["start_time"] = start_time
    match_dict["player1_id"] = player1_id
    match_dict["player2_id"] = player2_id

    match_dict["player1_score"] = player1_score
    match_dict["player2_score"] = player2_score

    match_dict["player1_name"] = player1_name
    match_dict["player2_name"] = player2_name

    match_dict["player1_elo_win"] = elo_at_stake(player1_elo,player2_elo)[0]
    match_dict["player1_elo_loss"] = - (elo_at_stake(player1_elo,player2_elo)[1])
    match_dict["player2_elo_win"] = elo_at_stake(player1_elo,player2_elo)[1]
    match_dict["player2_elo_loss"] = - (elo_at_stake(player1_elo,player2_elo)[0])


    match_dict["player1_elo"] = player1_elo
    match_dict["player2_elo"] = player2_elo

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


# ELO
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 18:11:27 2021

@author: mathiasrammhaugland
"""

def elo_at_stake(p1_ELO,p2_ELO):
    adv = 1800 #if you have adv more points than your opponent you are 10 times more likely to win
    k = 50

    pow1 = ((p1_ELO-p2_ELO)/adv)
    exp_score1 = 1/(1+10**pow1)
    p1_win = k*exp_score1 #p1_win is what p1 wins and p2 looses

    pow2 = ((p2_ELO-p1_ELO)/adv)
    exp_score2 = 1/(1+10**pow2)
    p2_win = k*exp_score2 #p2_win is what p2 wins and p1 looses

    return round(p1_win), round(p2_win)


def new_scores(p1_ELO,p2_ELO,winner): #winner is 'p1' or 'p2'
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

    if p2_ELO_new <=0:
        p2_ELO_new = 0

    return p1_ELO_new, p2_ELO_new




