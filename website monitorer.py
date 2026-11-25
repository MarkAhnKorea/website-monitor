import subprocess
import hashlib
import requests
import time
import tkinter as tk
import subprocess
from importlib import import_module
from pathlib import Path


app = tk.Tk()
app.withdraw()
current_popup = None

try:
    playsound = import_module("playsound").playsound
except ImportError:
    def playsound(sound_path):
        print(f"Audio notification unavailable: {sound_path}")

def popup():
    global current_popup
    if current_popup is not None and current_popup.poll() is None:
        return
    script = ('display dialog "Website content has changed!" '
              'with title "Website monitorer" '
              'buttons {"Close"} default button "Close"')
    current_popup = subprocess.Popen(["osascript", "-e", script])

def preference():
    choice = input("How would you like to be notified of changes? (sound/none/popup): ")
    if choice not in ["sound", "none", "popup"]:
        print("Invalid preference. Please choose 'sound', 'none', or 'popup'.")
        return preference()
    return choice

def play_sound():
    subprocess.run(["afplay", str(notification)], check=False)

website = input("Enter the website URL to monitor(without https://www.): ")
previous_hash = None
choice = preference()

notification = str(Path(__file__).resolve().parent / "notification.mp3")
frequency = int(input("How often would you like to check the website for changes? (in seconds): "))

while True:
    try:
        response = requests.get("https://www." + website, timeout=10)
        response.raise_for_status()
        current_hash = hashlib.md5(response.content).hexdigest()
        if previous_hash is None:
            previous_hash = current_hash
        if previous_hash != current_hash:
            print("Website content has changed")
            previous_hash = current_hash
            if choice == "sound":
                    play_sound()
            elif choice == "popup":
                popup()
        else:
            print("Website content has not changed")
    except requests.RequestException as e:
        print(f"Error occurred while accessing website: {e}")
    time.sleep(frequency)
