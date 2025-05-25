from flask import Flask, render_template, request, jsonify
import json
import os
import re

app = Flask(__name__)
ROUTES = []
with open("ettringen_all_routes.json", "r", encoding="utf-8") as f:
    ROUTES = json.load(f)


@app.route("/")
def index():
    return render_template("index.html.jinja2", routes=ROUTES)


def get_entry_by_name(data, name):
    value = None
    for item in data:
        if str(item["name"]).strip() == name:
            value = item
    if value == None:
        print(f"ERROR: Could not find {name}!")
        raise LookupError(f"Could not find {name}")
    return value


def grade_from_data(data):
    print(data)
    region = get_entry_by_name(ROUTES, data["region"])
    zone = get_entry_by_name(region["zones"], data["zone"])
    sector = get_entry_by_name(zone["sectors"], data["sector"])
    route = get_entry_by_name(sector["routes"], data["route"])
    return route["grade"]


@app.route("/save", methods=["POST"])
def save():
    data = request.json
    grade = grade_from_data(data)
    entry = {
        "region": data["region"],
        "zone": data["zone"],
        "sector": data["sector"],
        "route": data["route"],
        "date": data["date"],
        "attempt": data["attempt"],
        "grade": grade,
        "lead": data["lead"],
        "comment": data["comment"],
    }
    print(f'INFO: saving new entry: "{entry}"')
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


@app.template_filter("extract_grade_number")
def extract_grade_number(grade):
    match = re.search(r"^(\d+)", grade)
    return match.group(1) if match else "unknown"


@app.route("/logbook")
def logbook():
    if os.path.exists("logbook.json"):
        with open("logbook.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []
    return render_template("logbook.html.jinja2", logs=logs)
