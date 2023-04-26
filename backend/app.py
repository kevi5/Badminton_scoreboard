from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

last_player = None

@app.route("/update_score", methods=["POST"])
def update_score():
    global last_player
    data = request.json
    player = data.get("player", None)

    if player:
        last_player = player
        return jsonify({"success": True, "player": player})
    else:
        return jsonify({"success": False})

@app.route("/delete_previous_point", methods=["POST"])
def delete_previous_point():
    global last_player
    if last_player:
        player = last_player
        last_player = None
        return jsonify({"success": True, "player": player})
    else:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
