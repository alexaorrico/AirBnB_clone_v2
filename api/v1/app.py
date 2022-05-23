#!/usr/bin/python3
"""
Python flask
"""


from os import getenv
from flask import Flask,jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def close(bruh):
    """Method that calls close storage"""
    storage.close()


@app.errorhandler(404)
def error404(e):
    """ 404 handler """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(
            host=getenv('HBNB_API_HOST') or '0.0.0.0',
            port=int(getenv('HBNB_API_PORT') or 5000),
            threaded=True
        )
