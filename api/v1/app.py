#!/usr/bin/python3
"""
file app for starting FLask
registering blueprint
"""
from os import getenv
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """
    to close query zfter each session
    """
    storage.close()


# @app.errorhandler(404)
# def not_found(error):
#     '''
#     return JSON formatted 404 status code response
#     '''
#     return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """ app listening on host 0.0.0.0 and port 5000 """
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')), threaded=True)
