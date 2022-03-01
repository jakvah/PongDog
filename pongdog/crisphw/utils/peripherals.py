import requests, os, wget, imghdr

def fetch_player_image(playerID):
    if os.path.isfile("images/profilepictures/"+str(playerID)+".png") or os.path.isfile("images/profilepictures/"+str(playerID)+".jpg"):
        print("Profile picture already exists.")
        #return
    response = requests.get("https://jakvah.pythonanywhere.com/static/imgs/"+str(playerID))
    print(response.status_code)
    if response.status_code != 200:
        print("Profile picture does not exist on server")
        #return
    
    print(imghdr.what("oi", h=response.content))
    #^bruk den her til å finne ut om du skal lagre som png eller jpg!

    filejpg = open("images/profilepictures/"+str(playerID)+".jpg", "wb")
    filejpg.write(response.content)
    filejpg.close()
    # - png 
    filepng = open("images/profilepictures/"+str(playerID)+".png", "wb")
    filepng.write(response.content)
    filepng.close()
    print(imghdr.what("images/profilepictures/317094323.jpg",h=response.content))


if __name__ == "__main__":
    fetch_player_image(2)

