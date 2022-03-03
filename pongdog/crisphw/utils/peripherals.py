import requests, os, wget, imghdr

def fetch_player_image(playerID):
    if os.path.isfile("images/profilepictures/"+str(playerID)+".png") or os.path.isfile("images/profilepictures/"+str(playerID)+".jpg"):
        print("Profile picture already exists.")
        return
    response = requests.get("https://jakvah.pythonanywhere.com/static/imgs/"+str(playerID))
    if response.status_code != 200:
        print("Profile picture does not exist on server")
        return
    print("Fetching profile picture..")
    if imghdr.what("oi", h=response.content) == "png":
        print("saving as " +str(playerID)+".png")
        filepng = open("images/profilepictures/"+str(playerID)+".png", "wb")
        filepng.write(response.content)
        filepng.close()
    elif imghdr.what("oi", h=response.content) == "jpg":
        print("saving as " +str(playerID)+".jpg")
        filejpg = open("images/profilepictures/"+str(playerID)+".jpg", "wb")
        filejpg.write(response.content)
        filejpg.close()

    # - png 

if __name__ == "__main__":
    fetch_player_image(317094323)

