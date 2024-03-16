from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "<h1>HMM-Scaler: Scaling Detector</h1>", 200