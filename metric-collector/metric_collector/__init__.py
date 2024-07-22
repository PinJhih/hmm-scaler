from flask import Flask, request, jsonify

from .collector import Collector

app = Flask(__name__)
collector = Collector(app)


@app.route("/", methods=["GET"])
def index():
    return "<h1>HMM-Scaler: Metric Collector</h1>", 200


@app.route("/interval/<int:t>", methods=["PUT"])
def set_interval(t):
    collector.set_interval(t)
    msg = {"message": f"Interval is set to {t}"}
    return jsonify(msg), 200


@app.route("/targets", methods=["PUT"])
def set_targets():
    targets = request.get_json()
    collector.set_targets(targets)
    msg = {"message": f"targets are updated"}
    return jsonify(msg), 200


@app.route("/prom", methods=["PUT"])
def set_prom():
    url = request.get_json()["url"]
    collector.set_prom(url)

    msg = {"message": f"Prom url is set to {url}"}
    return jsonify(msg), 200
