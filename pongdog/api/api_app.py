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
        return "200"
    else:
        return "300"


@app.route("/increment_score/<player_num>")
def increment_score(player_num):
    if not int(player_num) in [1,2]:
        return "300" # Invalid player num (not 1 or 2)
    else:
        if dbm.increment_score(int(player_num)):
            return "200" # Success
        else:
            return "400"



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



# FROM: https://github.com/hermabe/rfid-card
# Reverses CARD EM number to RFID number
def reverseBytes(number):
    binary = "{0:0>32b}".format(number) # Zero-padded 32-bit binary
    byteList = [binary[i:i+8][::-1] for i in range(0, 32, 8)] # Reverse each byte
    return int(''.join(byteList), 2) # Join and convert to decimal
    # return int(''.join(["{0:0>32b}".format(number)[i:i+8][::-1] for i in range(0, 32, 8)]), 2)


