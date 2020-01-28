#!/usr/bin/python3
"""File"""

from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/api/v1/status')
def status():
    """Route /status on the object app_views that returns a
     JSON: "status": "OK"""""
    status = {"status": "OK"}
    return jsonify(status)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or "0.0.0.0"
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True, debug=True)
