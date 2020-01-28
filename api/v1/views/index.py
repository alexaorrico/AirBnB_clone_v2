from api.v1.views import app_views
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/status')
def status():
    """
    create a route /status on the object app_views
    that returns a JSON: "status": "OK"
    """
    return jsonify(status="OK")
