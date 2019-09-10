#!/usr/bin/python3

from flask import Flask, Blueprint, render_template, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

@app.errorhandler(404)
def error(e):
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
