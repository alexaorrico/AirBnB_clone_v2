#!/usr/bin/python3
"""
    to create a flask api application
"""

import os
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={
            r'/*': {'origins': os.getenv('HBNB_API_HOST', '0.0.0.0')}})


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(code):
    """
    teardown_appcontext method that closes the storage
    """
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """Handler for 404 Not found errors"""
    return ({'error': 'Not found'}), 404

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    # getenv returns a string and port is an int
    # THREADED is set to true
    app.run(host=host, port=port, threaded=True)
