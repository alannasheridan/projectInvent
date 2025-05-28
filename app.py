from flask import Flask, render_template, request, jsonify
import json
import os
import platform
from gpio_listener import start_gpio_thread  # Only activates on Raspberry Pi

app = Flask(__name__)

# Load sound mappings
with open("sounds.json") as f:
    sound_map = json.load(f)

@app.route("/")
def index():
    available_sounds = os.listdir("sounds")
    return render_template("index.html", sounds=sound_map, available_sounds=available_sounds)

@app.route("/play", methods=["GET"])
def play_sound():
    sound = request.args.get("sound")
    if sound and sound in os.listdir("sounds"):
        os.system(f"afplay sounds/{sound}")  # Replace with 'omxplayer' on Raspberry Pi
        return "Playing sound..."
    return "Invalid sound"

@app.route("/update", methods=["POST"])
def update_sound():
    data = request.json
    sound_map[data["button"]] = data["sound"]
    with open("sounds.json", "w") as f:
        json.dump(sound_map, f, indent=4)
    return jsonify(success=True)

def play_mapped_sound(button):
    sound_file = sound_map.get(button)
    if sound_file:
        os.system(f"afplay sounds/{sound_file}")  # Replace with 'omxplayer' on Raspberry Pi

if __name__ == "__main__":
    if platform.system() == "Linux":
        start_gpio_thread(play_mapped_sound)
    else:
        print("Running on non-Raspberry Pi system — GPIO disabled.")

    app.run(debug=True)
