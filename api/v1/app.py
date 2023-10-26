#!/usr/bin/python3
"""creating api with flask"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_down(exception):
    """documented function"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """handle page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
