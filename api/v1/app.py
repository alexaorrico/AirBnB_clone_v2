#!/usr/bin/python3
"""module containing main app"""
import json
from flask import Flask, jsonify
from sqlalchemy.sql.operators import json_path_getitem_op
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def refresh(exception):
    """refresh storage"""
    storage.close()


@app.errorhandler(404)
def four_o_4(exception):
    """handles 404 error"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if (not host):
        host = "0.0.0.0"
    if (not port):
        port = 5000
    app.run(host=host, port=port, threaded=True)
