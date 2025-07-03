# from flask import Flask, render_template, request, jsonify
# import json
# import os
# import platform

# app = Flask(__name__)

# # Load sound mappings
# with open("sounds.json") as f:
#     sound_map = json.load(f)

# DISPLAY_NAMES = {
#     "beep.mp3": "Beep",
#     "bubble.mp3": "Bubble Pop",
#     "pop.mp3": "Click Pop",
#     "whoosh.mp3": "Wind Whoosh"
# }

# # Cross-platform audio playback
# if platform.system() == "Linux":
#     def play_audio(file):
#         os.system(f"omxplayer sounds/{file}")
# else:
#     import pygame
#     pygame.init()
#     def play_audio(file):
#         pygame.mixer.music.load(f"sounds/{file}")
#         pygame.mixer.music.play()

# @app.route("/")
# def index():
#     available_sounds = os.listdir("sounds")
#     return render_template("index.html", sounds=sound_map, available_sounds=available_sounds, display_names=DISPLAY_NAMES)

# @app.route("/play", methods=["GET"])
# def play_sound():
#     sound = request.args.get("sound")
#     if sound and sound in os.listdir("sounds"):
#         play_audio(sound)
#         return "Playing sound..."
#     return "Invalid sound"

# @app.route("/update", methods=["POST"])
# def update_sound():
#     data = request.json
#     sound_map[data["button"]] = data["sound"]
#     with open("sounds.json", "w") as f:
#         json.dump(sound_map, f, indent=4)
#     return jsonify(success=True)

# if __name__ == "__main__":
#     print("Running on Raspberry Pi" if platform.system() == "Linux" else "Running on non-Raspberry Pi system — GPIO disabled.")
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import json
import os
import platform
import threading
import time

app = Flask(__name__)

# Load sound mappings from JSON
with open("sounds.json") as f:
    sound_map = json.load(f)

# Friendly display names for dropdowns (optional)
DISPLAY_NAMES = {
    "beep.mp3": "Beep",
    "bubble.mp3": "Bubble Pop",
    "pop.mp3": "Click Pop",
    "whoosh.mp3": "Wind Whoosh"
}

# Determine OS and define playback method
if platform.system() == "Linux":
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

    # GPIO pin to button label mapping
    gpio_to_button = {
        17: "Button 1",
        27: "Button 2",
        22: "Button 3",
        23: "Button 4",
        5:  "Toggle 1",
        6:  "Toggle 2",
        13: "Toggle 3",
        19: "Toggle 4"
    }

    for pin in gpio_to_button:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def play_audio(file):
        os.system(f"omxplayer sounds/{file} > /dev/null 2>&1")

    # Start a thread that listens for GPIO input
    def gpio_listener():
        while True:
            for pin, button_name in gpio_to_button.items():
                if GPIO.input(pin):
                    sound_file = sound_map.get(button_name)
                    if sound_file:
                        play_audio(sound_file)
                    time.sleep(0.3)  # debounce
    threading.Thread(target=gpio_listener, daemon=True).start()

else:
    import pygame
    pygame.init()
    def play_audio(file):
        pygame.mixer.music.load(f"sounds/{file}")
        pygame.mixer.music.play()

@app.route("/")
def index():
    available_sounds = os.listdir("sounds")
    return render_template("index.html", sounds=sound_map, available_sounds=available_sounds, display_names=DISPLAY_NAMES)

@app.route("/play", methods=["GET"])
def play_sound():
    sound = request.args.get("sound")
    if sound and sound in os.listdir("sounds"):
        play_audio(sound)
        return "Playing sound..."
    return "Invalid sound"

@app.route("/update", methods=["POST"])
def update_sound():
    data = request.json
    sound_map[data["button"]] = data["sound"]
    with open("sounds.json", "w") as f:
        json.dump(sound_map, f, indent=4)
    return jsonify(success=True)

if __name__ == "__main__":
    print("Running on Raspberry Pi" if platform.system() == "Linux" else "Running on non-Raspberry Pi system — GPIO disabled.")
    app.run(debug=True, host="0.0.0.0")  # host="0.0.0.0" makes it accessible on local network