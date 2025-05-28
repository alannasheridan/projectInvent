from flask import Flask, render_template, request, jsonify
import json
import os
# from gpio_listener import start_gpio_thread 

app = Flask(__name__)

# Load sound mappings
with open("sounds.json") as f:
    sound_map = json.load(f)

@app.route("/")
def index():
    available_sounds = os.listdir("sounds")  # <-- NEW
    return render_template("new.html", sounds=sound_map, available_sounds=available_sounds)  # <-- UPDATED

@app.route("/play", methods=["GET"])
def play_sound():
    sound = request.args.get("sound")
    if sound and sound in os.listdir("sounds"):  # <-- UPDATED
        os.system(f"afplay sounds/{sound}")  # change to 'omxplayer' on Raspberry Pi
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
    import platform

    if platform.system() == "Linux":
        from gpio_listener import start_gpio_thread
        start_gpio_thread(play_mapped_sound)
    else:
        print("Running on non-Raspberry Pi system — GPIO disabled.")

    app.run(debug=True)