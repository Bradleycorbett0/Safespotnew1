import requests

FIREBASE_URL = "https://safespot-c5e02-default-rtdb.firebaseio.com"

def save_to_firebase(endpoint, data):
    url = f"{FIREBASE_URL}/{endpoint}.json"
    response = requests.post(url, json=data)
    return response.ok

def get_from_firebase(endpoint):
    url = f"{FIREBASE_URL}/{endpoint}.json"
    response = requests.get(url)
    if response.ok and response.json():
        return response.json()
    return {}