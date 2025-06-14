import json
import os

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def login_user(email, password):
    users = load_users()
    if email in users and users[email] == password:
        return True, "Login successful."
    return False, "Invalid email or password."

def register_user(email, password):
    users = load_users()
    if email in users:
        return False, "Email already registered."
    users[email] = password
    save_users(users)
    return True, "Registration successful."