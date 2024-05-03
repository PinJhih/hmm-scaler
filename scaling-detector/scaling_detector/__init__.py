from flask import Flask, jsonify, request

from .controllers.detector import Detector

app = Flask(__name__)
detector = Detector()


@app.route("/", methods=["GET"])
def index():
    return "<h1>HMM-Scaler: Scaling Detector</h1>", 200


@app.route("/detect", methods=["POST"])
def detect():
    metrics = request.json
    detector.detect(metrics)
    msg = {"message": "OK!"}
    return jsonify(msg), 200
