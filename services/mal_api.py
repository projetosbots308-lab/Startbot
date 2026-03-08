import requests

BASE = "https://api.jikan.moe/v4"

def search_anime(name):
    r = requests.get(f"{BASE}/anime?q={name}&limit=1")
    return r.json()

def search_manga(name):
    r = requests.get(f"{BASE}/manga?q={name}&limit=1")
    return r.json()

def season_now():
    r = requests.get(f"{BASE}/seasons/now")
    return r.json()
