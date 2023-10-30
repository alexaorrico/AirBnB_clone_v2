#!/usr/bin/python3
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    return storage.close()


@app.errorhandler(404)
def pageNotFound():
    error = jsonify({
        "error": "Not found"
    })
    error.status_code = 404
    return error


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
