from flask import Flask, request
from .controllers.collector import Collector

app = Flask(__name__)
collector = Collector(app)

@app.route("/", methods=["GET"])
def index():
    return "<h1>HMM-Scaler: Metric Collector</h1>", 200


@app.route("/interval/<int:t>", methods=["PUT"])
def set_interval(t):
    return collector.set_interval(t)


@app.route("/targets", methods=["PUT"])
def set_targets():
    targets = request.get_json()
    return collector.set_targets(targets)
