#!/usr/bin/python3
"""
App file of the program
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_404(error):
    """error 404 Not found"""
    return (jsonify(error="Not found"), 404)

@app.teardown_appcontext
def close_sesssion(_):
    storage.close()

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host, port, threaded=True)
