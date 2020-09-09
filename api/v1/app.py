#!/usr/bin/python3
"""make api"""
from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """teardown method"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """404 error handler

    args:
        error status
    return:
        json error response
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host, port, threaded=True)
