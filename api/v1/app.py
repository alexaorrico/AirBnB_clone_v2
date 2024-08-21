#!/usr/bin/python3
""" Creating the Flask App """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """404 error handler"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':

    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(debug=True, host=host, port=port, threaded=True)
