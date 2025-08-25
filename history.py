import os
import json

HISTORY_FILE = "chat_history.json"
conversation = []

def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(conversation, f)

def load_history():
    global conversation
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            conversation = json.load(f)

def clear_history():
    global conversation
    conversation = []
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
