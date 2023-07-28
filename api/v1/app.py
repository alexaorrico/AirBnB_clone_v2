#!/usr/bin/python3
"""

"""
import os
import models
from api.v1.views import app_views
from flask import Flask, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(error):
    """404 Error Handler"""
    print(error)
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def teardown(exception=None):
    models.storage.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", '0.0.0.0')
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
