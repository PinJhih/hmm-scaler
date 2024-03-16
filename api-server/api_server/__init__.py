from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "<h1>HMM-Scaler: API Server</h1>", 200
