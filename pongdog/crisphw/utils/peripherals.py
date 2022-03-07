import requests, os, imghdr
import numpy as np
from PIL import Image, ImageDraw


def convert_image_to_cropped_png(playerID, filetype):
    print("Cropping image.")
    img=Image.open("images/profilepictures/"+str(playerID)+"."+str(filetype)).convert("RGB")
    
    size = min(img.size)

    originX = img.size[0] / 2 - size / 2
    originY = img.size[1] / 2 - size / 2

    cropBox = (originX, originY, originX + size, originY + size)
    cropped = img.crop(cropBox)
    h,w = cropped.size
    npImage=np.array(cropped)

    # Create same size alpha layer with circle
    alpha = Image.new('L', cropped.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save('images/profilepictures/'+str(playerID)+".png")
    print("Done!")
    return

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
        convert_image_to_cropped_png(playerID,"png")
        return
    elif imghdr.what("oi", h=response.content) == "jpg":
        print("saving as " +str(playerID)+".jpg")
        filejpg = open("images/profilepictures/"+str(playerID)+".jpg", "wb")
        filejpg.write(response.content)
        filejpg.close()
        convert_image_to_cropped_png(playerID,"jpg")
        return
    else: #Unknown filetype?
        filejpg2 = open("images/profilepictures/"+str(playerID)+".jpg", "wb")
        filejpg2.write(response.content)
        filejpg2.close()
        print(playerID)
        convert_image_to_cropped_png(playerID,"jpg")
        return

def get_name_and_elo(playerID):
    url = f"https://jakvah.pythonanywhere.com/get_player_overview/{playerID}"
    try:
        response = requests.get(url)
        data = response.json()
        print(data['name'],data['elo'])
        return data['name'], int(data['elo'])
    except:
        print("Could not fetch data. Player exists?")
        return 0,0

def post_winner(winner, loser):
    url = f"https://jakvah.pythonanywhere.com/add_result/{winner}/{loser}"
    r = requests.post(url)
    print(r.text)
    if r.text == "200":
        return True
    else:
        return False