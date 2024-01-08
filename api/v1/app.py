#!/usr/bin/python3
from flask import Flask, render_template, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


def teardown_appcontext(exception):
    """
    Method to close storage
    """
    storage.close()


@app.errorhandler(404)
def return_404(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
