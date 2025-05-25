from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)


@app.route("/")
def index():
    with open("ettringen_all_routes.json", "r", encoding="utf-8") as f:
        routes = json.load(f)
    return render_template("index.html", routes=routes)


@app.route("/save", methods=["POST"])
def save():
    data = request.json
    print(data)
    entry = {
        "region": data["region"],
        "zone": data["zone"],
        "sector": data["sector"],
        "route": data["route"],
        "date": data["date"],
        "attempt": data["attempt"],
        "lead": data["lead"],
        "comment": data["comment"],
    }
    log_file = "logbook.json"
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, sort_keys=True, indent=4)
    return jsonify(success=True)


@app.route("/logbook")
def logbook():
    if os.path.exists("logbook.json"):
        with open("logbook.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []
    return render_template("logbook.html", logs=logs)
