#!/usr/bin/python3
""" App module """
import os
from flask import Flask, jsonify
from flask import make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})
CORS(app, resources={r"/*": {"origins": "http://0.0.0.0:*"}})


@app.teardown_appcontext
def teardown_appcontext(response_or_exc):
    """ Tear down function """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 - Not found function """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST') or "0.0.0.0"
    port = os.environ.get('HBNB_API_PORT') or '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
