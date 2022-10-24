#!/usr/bin/python3

""" The main flask app for the endpoint """
from os import getenv
from flask import Flask, jsonify, request
from models import storage
from api.v1.views import app_views
from flask import make_response
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins":"0.0.0.0"}})

@app.errorhandler(404)
def _handle_api_error(ex):
    if request.path.startswith('/api/v1/'):
        return jsonify({"error": "Not found"})
    else:
        return ex


@app.teardown_appcontext
def tear_down(exc):
    storage.close()


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', 5000),
            threaded=True)
