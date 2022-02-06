#!/usr/bin/python3
"""
Returns status of API
"""
import os
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardowwn_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()

@app.errorhandler(404)
def page_err(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
