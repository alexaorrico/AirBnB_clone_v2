#!/usr/bin/python3
"""This module creates the Flask application"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorshandler(404)
def errorshandler(error):
    """error handler"""
    return (
        "Not found",
        404,
    )


@app.teardown_appcontext
def teardown(exception):
    """close the database storage"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    
    app.run(host=host, port=port, threaded=True)
