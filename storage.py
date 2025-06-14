import json
import os

DATA_DIR = '/storage/emulated/0/safespot/data'

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_json(filename):
    ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def save_json(filename, data):
    ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)