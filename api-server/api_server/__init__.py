from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "<h1>HMM-Scaler: API Server</h1>", 200


@app.route("/config", methods=["GET"])
def get_config():
    # TODO: call method of controllers
    config = {
        "interval": 30,
        "targets": [
            {
                "namespace": "social-network",
                "names": [
                    "compose-post-service",
                    "home-timeline-redis",
                    "home-timeline-service",
                ],
            },
        ],
    }
    return jsonify(config), 200


@app.route("/interval", methods=["GET"])
def get_interval():
    # TODO: call method of controllers
    interval = {"interval": 30}
    return jsonify(interval), 200


@app.route("/interval/<int:t>", methods=["PUT"])
def set_interval(t):
    # TODO: call method of controllers
    msg = {"message": f"interval is set to {t}"}
    return jsonify(msg), 200


@app.route("/targets", methods=["GET"])
def get_targets():
    # TODO: call method of controllers
    targets = [
        {
            "namespace": "social-network",
            "names": [
                "compose-post-service",
                "home-timeline-redis",
                "home-timeline-service",
            ],
        },
    ]
    return jsonify(targets), 200


@app.route("/targets/<string:ns>/<string:name>", methods=["POST"])
def add_target(ns, name):
    # TODO: call method of controllers
    msg = {"message": f"{name} in {ns} is added"}
    return jsonify(msg), 200


@app.route("/targets/<string:ns>/<string:name>", methods=["DELETE"])
def delete_target(ns, name):
    # TODO: call method of controllers
    msg = {"message": f"{name} in {ns} is deleted"}
    return jsonify(msg), 200
