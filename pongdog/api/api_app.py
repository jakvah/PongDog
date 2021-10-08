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





# FROM: https://github.com/hermabe/rfid-card
# Reverses CARD EM number to RFID number
def reverseBytes(number):
    binary = "{0:0>32b}".format(number) # Zero-padded 32-bit binary
    byteList = [binary[i:i+8][::-1] for i in range(0, 32, 8)] # Reverse each byte
    return int(''.join(byteList), 2) # Join and convert to decimal
    # return int(''.join(["{0:0>32b}".format(number)[i:i+8][::-1] for i in range(0, 32, 8)]), 2)

