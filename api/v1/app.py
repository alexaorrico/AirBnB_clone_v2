#!/usr/bin/python3
"""Flask web service API"""

from flask import Flask, make_response, jsonify

import os
from models import storage
from api.v1.views import app_views  # Blueprint

app = Flask(__name__)

# Register app_views as blueprint to app
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error=None):
    """ Called when application context is torn down"""
    storage.close()

@app.errorhandler(404)  # 404 Responds handler for unavailable resources
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=(os.getenv('HBNB_API_HOST', '0.0.0.0')),
            port=(int(os.getenv('HBNB_API_PORT', '5000'))),
            threaded=True, debug=True)
