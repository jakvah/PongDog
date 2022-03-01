import requests, os

def fetch_player_image(playerID):
    if os.path.isfile("images/profilepictures/"+str(playerID)+".png") or os.path.isfile("images/profilepictures/"+str(playerID)+".jpg"):
        print("Profile picture already exists.")
        return
    response = requests.get("https://jakvah.pythonanywhere.com/static/imgs/"+str(playerID))
    file = open("images/profilepictures/"+str(playerID)+".png", "wb")
    file.write(response.content)
    file.close()

if __name__ == "__main__":
    fetch_player_image(2)