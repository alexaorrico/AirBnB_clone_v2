#!/usr/bin/python3
"""
App with Flask 
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Returns a error 404"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', base='0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', base=5000))
    app.run(host=host, port=int(port), threaded=True)
