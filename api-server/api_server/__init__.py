from flask import Flask, request, send_file

from pathlib import Path

from .controllers import config_mgr


CURRENT_DIR = str(Path(__file__).parent.resolve())
STATIC_PATH = f"{CURRENT_DIR}/static"

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return send_file(STATIC_PATH + '/index.html')


@app.route("/config", methods=["GET"])
def get_config():
    return config_mgr.get_config()


@app.route("/interval", methods=["GET"])
def get_interval():
    return config_mgr.get_interval()


@app.route("/interval/<int:t>", methods=["PUT"])
def set_interval(t):
    return config_mgr.set_interval(t)


@app.route("/targets", methods=["GET"])
def get_targets():
    return config_mgr.get_targets()


@app.route("/targets/<string:ns>/<string:name>", methods=["POST"])
def add_target(ns, name):
    return config_mgr.add_target(ns, name)


@app.route("/targets/<string:ns>/<string:name>", methods=["DELETE"])
def delete_target(ns, name):
    return config_mgr.delete_target(ns, name)


@app.route("/prom", methods=["PUT"])
def set_prom():
    url = request.get_json()["url"]
    return config_mgr.set_prom(url)


@app.route("/prom", methods=["GET"])
def get_prom():
    return config_mgr.get_prom()
