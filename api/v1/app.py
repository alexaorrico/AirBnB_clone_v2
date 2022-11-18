#!/usr/bin/python3
'''Flask web API.
'''
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
'''Flask application instance.'''


@app.teardown_appcontext
def teardown_flask(exception):
    '''method to handle @app.teardown_appcontext'''
    storage.close()

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    app.url_map.strict_slashes = False
    app.register_blueprint(app_views)
    app.run(
        host=host if host else '0.0.0.0',
        port=port if port else '5000',
        threaded=True
    )
