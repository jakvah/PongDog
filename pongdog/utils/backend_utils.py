"""
Utils for the PongDog Backend hosted at jakvah.pythonanywhere.com
"""

import requests


def get_player_overview(player_id):
    url = f"https://jakvah.pythonanywhere.com/get_player_overview/{player_id}"
    r = requests.get(url)
    data = r.json()
    return int(data["elo"]), str(data["name"])

def add_result(p1_id,p2_id,p1_score,p2_score):
    if p1_score > p2_score:
        url = f"https://jakvah.pythonanywhere.com/add_result/{p1_id}/{p2_id}"
    else:
        url = f"https://jakvah.pythonanywhere.com/add_result/{p2_id}/{p1_id}"
    
    try:
        r = requests.post(url)
        return r.text
    except Exception as e:
        raise e

