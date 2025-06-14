# firebase.py
import pyrebase

firebase_config = {
    "apiKey": "AIzaSyBe2zwZNcPtM8k0FCkEShmYnhB1q5PiMlg",
    "authDomain": "safespot-c5e02.firebaseapp.com",
    "projectId": "safespot-c5e02",
    "storageBucket": "safespot-c5e02.appspot.com",
    "messagingSenderId": "181446649081",
    "appId": "1:181446649081:web:d865f095d6dad62d90b9a5",
    "measurementId": "G-DC1D27DY1F",
    "databaseURL": "https://safespot-c5e02-default-rtdb.firebaseio.com"  # Make sure Realtime Database is enabled in Firebase
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

def save_spot(spot_data):
    db.child("spots").push(spot_data)

def get_spots():
    data = db.child("spots").get()
    if data.each():
        return [item.val() for item in data.each()]
    return []

def save_comment(comment_data):
    db.child("comments").push(comment_data)

def get_comments():
    data = db.child("comments").get()
    if data.each():
        return [item.val() for item in data.each()]
    return []

def save_contact(contact_data):
    db.child("contacts").push(contact_data)

def get_contacts():
    data = db.child("contacts").get()
    if data.each():
        return [item.val() for item in data.each()]
    return []