#!/usr/bin/python3
"""Flask"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(session):
    """close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Eror 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
