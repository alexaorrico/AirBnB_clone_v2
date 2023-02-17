#!/usr/bin/python3
'''Run Flask application API
'''
from models import storage
import os
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown_flask(exception):
    '''method that handles teardown'''
    # print(exception)
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''handles 404 error code'''
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    '''handles 400 error code'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
