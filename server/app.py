import pyrebase
import json
from helper_function import helper
from flask import Flask, request, jsonify, request
from flask_cors import CORS, cross_origin
from database import DB
import json

conn, cur = helper.initialize_database()
db = DB(conn, cur)
db.create_user_table()
db.create_award_table()
db.create_challenge_table()

app = Flask(__name__)
CORS(app)
app.config["CORS_ORIGINS"] = ["http://localhost:8080", "http://127.0.0.1:5000", "http://localhost:3000"]
app.config['JSON_SORT_KEYS'] = False

@app.route("/register-user", methods=["POST", "GET"])
def register_user():
    data = json.loads(request.data)
    db.add_user(data["uid"], data["user_name"])
    return "user added"

@app.route("/create-challenge", methods=["POST"])
def create_challenge():
    data = json.loads(request.data)
    db.create_challenge(data["challenge_name"], data["award"], data["description"], data["end_time"])
    return "event added"

if __name__ == '__main__':
	app.run(debug=True, port=3001)


# @app.route("/result", methods=["POST", "GET"])
# def result():