#!/usr/bin/python3
'''Flask application module'''


from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown(exception):
    '''what should happen when the app is getting teared down'''
    if storage is not None:
        storage.close()


@app.errorhandler(404)
def errorhandler(error):
    '''404 error handler'''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
