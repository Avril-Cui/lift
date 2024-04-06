import json
from helper_function import helper
from flask import Flask, request, jsonify, request
from flask_cors import CORS, cross_origin
from db_commands import dbCommands
import json

conn, cur = helper.initialize_database()
db_function = dbCommands(conn, cur)
# db_function.create_joined_challenge_table()
# db_function.create_user_table()
# db_function.create_award_table()
# db_function.create_challenge_table()

app = Flask(__name__)
CORS(app)
app.config["CORS_ORIGINS"] = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_SORT_KEYS'] = False

@app.route("/register-user", methods=["POST"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def register_user():
    data = json.loads(request.data)
    db_function.add_user(data["uid"], data["user_name"])
    return jsonify("signed up success")

@app.route("/create-challenge", methods=["POST"])
@cross_origin(origin='localhost',headers=['Content-Type'])
def create_challenge():
    data = json.loads(request.data)
    db_function.create_challenge(data["challenge_name"], data["award"],
                        data["description"], data["is_time"], data["end_time"], data["target"])
    return "event added"

@app.route("/get-challenge", methods=["GET"])
@cross_origin(origin='localhost',headers=['Content-Type'])
def get_challenge():
    challenge = db_function.get_challenge()
    return challenge

@app.route("/get-user-name", methods=["GET"])
def get_user_name():
    user_uid = json.loads(request.data)
    user_name = db_function.get_user_name(user_uid)
    return jsonify(user_name)

@app.route("/get-user-stats", methods=["POST"])
@cross_origin(origin='localhost',headers=['Content-Type'])
def get_user_stats():
    user_uid = json.loads(request.data)
    result = db_function.get_user_stats(user_uid)
    return jsonify(result)

@app.route('/join-challenge', methods=["POST"])
def join_challenge():
    data2 = json.loads(request.data)
    db_function.join_challenge(data2['uid'], data2['user_name'], data2['challenge_id'])
    return "challenge joined!"

@app.route('/get-challenge-rank', methods=["POST"])
def get_challenge_rank():
    challenge_id = json.loads(request.data)
    rank = db_function.get_challenge_rank(challenge_id)
    return rank

@app.route('/find-challenge', methods=["POST"])
def find_challenge():
    challenge_id = json.loads(request.data)
    challenge = db_function.find_challenge(challenge_id)
    return jsonify(challenge)

@app.route('/is-joined', methods=["POST"])
def is_joined():
    data1 = json.loads(request.data)
    challenge_join = db_function.join_data(data1["user_uid"], data1["challenge_id"])
    if challenge_join["data_result"] != None:
        return "true"
    else:
        return "false"

@app.route('/joined-data', methods=["POST"])
def joined_data():
    data = json.loads(request.data)
    challenge1 = db_function.join_data(data["user_uid"], data["challenge_id"])
    return jsonify(challenge1)

@app.route('/change-data', methods=["POST"])
def change_data():
    data3 = json.loads(request.data)
    print(data3)
    db_function.update_data(data3["current_progress"], data3["challenge_id"], data3["user_uid"])
    return "current progress updated"

@app.route('/join-rank', methods=["POST"])
def join_rank():
    data = json.loads(request.data)
    join_rank = db_function.join_rank(data["user_uid"], data["challenge_id"])
    return join_rank

@app.route('/find-joined-challenge', methods=["POST"])
def find_joined_challenge():
    data = json.loads(request.data)
    joined_challenge = db_function.find_joined_challenge(data)
    return joined_challenge

@app.route('/update-reps', methods=["POST"])
def update_reps():
    data = json.loads(request.data)
    db_function.update_reps(data["user_uid"], data["reps"])
    return "updated"

@app.route('/update-calories', methods=["POST"])
def update_calories():
    data = json.loads(request.data)
    db_function.update_calories(data["user_uid"], data["calories"])
    return "updated"

@app.route('/update-time', methods=["POST"])
def update_time():
    data = json.loads(request.data)
    db_function.update_time(data["user_uid"], data["time"])
    return "updated"

if __name__ == '__main__':
    app.run(debug=True, port=3001, host="localhost")

