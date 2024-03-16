from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "<h1>HMM-Scaler: Metric Collector</h1>", 200


@app.route("/interval/<int:t>", methods=["PUT"])
def set_interval(t):
    # TODO: call method of controllers
    msg = {"message": f"interval is set to {t}"}
    return jsonify(msg), 200


@app.route("/targets", methods=["PUT"])
def set_targets():
    # TODO: call method of controllers
    targets = request.get_json()
    msg = {"message": f"targets is updated"}
    return jsonify(msg), 200
