import pandas as pd
from flask import Flask, jsonify, request


from .controllers.detector import Detector

app = Flask(__name__)
detector = Detector()


@app.route("/", methods=["GET"])
def index():
    return "<h1>HMM-Scaler: Scaling Detector</h1>", 200


@app.route("/detect", methods=["POST"])
def detect():
    try:
        body = request.json
        metrics = pd.DataFrame(body["metrics"])
        metrics.index = metrics.index.map(eval)
        response_time = body["response_time"]
    except:
        msg = {"message": "Format error!"}
        return jsonify(msg), 400

    detector.detect(metrics, response_time)
    msg = {"message": "OK!"}
    return jsonify(msg), 200
