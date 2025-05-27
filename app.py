from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load sound mappings
with open("sounds.json") as f:
    sound_map = json.load(f)

@app.route("/")
def index():
    return render_template("index.html", sounds=sound_map)

@app.route("/play", methods=["GET"])
def play_sound():
    sound = request.args.get("sound")
    if sound and sound in sound_map.values():
        os.system(f"afplay sounds/{sound}")  # use 'afplay' on Mac or 'start' on Windows
        return "Playing sound..."
    return "Invalid sound"

@app.route("/update", methods=["POST"])
def update_sound():
    data = request.json
    sound_map[data["button"]] = data["sound"]
    with open("sounds.json", "w") as f:
        json.dump(sound_map, f, indent=4)
    return jsonify(success=True)