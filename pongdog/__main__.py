# -*- coding: utf-8 -*- 
from flask import Flask, request, render_template, Markup,flash,redirect
import requests

app = Flask(__name__)
app.secret_key = "super secret key"
#CORS(app)
NUM_TABS = 3


@app.route("/")
def index():
    return redirect("/pongdog/register")

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

@app.route("/test")
def test():
    return render_template("test.html")


# FROM: https://github.com/hermabe/rfid-card
# Reverses CARD EM number to RFID number
def reverseBytes(number):
    binary = "{0:0>32b}".format(number) # Zero-padded 32-bit binary
    byteList = [binary[i:i+8][::-1] for i in range(0, 32, 8)] # Reverse each byte
    return int(''.join(byteList), 2) # Join and convert to decimal
    # return int(''.join(["{0:0>32b}".format(number)[i:i+8][::-1] for i in range(0, 32, 8)]), 2)


if __name__ == '__main__':
    # Set debug false if it is ever to be deployed
    app.run(debug=True) 