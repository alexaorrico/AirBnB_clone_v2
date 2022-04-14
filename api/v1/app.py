#!/usr/bin/python3
"""
Hbnb module app.y
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontex(ctx):
    """
    calls storage.close
    """
    storage.close()


@app.errorhandler(404)
def page_not_found_error_handler(error):
    """
    Handle 404 case when a page is not found
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')),
            threaded=True)
