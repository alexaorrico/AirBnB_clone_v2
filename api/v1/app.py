#!/usr/bin/python3
"""init app flask object and runs app"""
from flask import Flask, jsonify
from models import storage
# hasn't been created yet
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


# register blueprint app_views to app ?
@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    status = {
        "error": "Not found"
    }
    return jsonify(status), 404


if __name__ == "__main__":
    # need to set these to HBNB_API_HOST and HBNB_API_PORT
    if environ['HBNB_API_HOST'] is None:
        environ['HBNB_API_HOST'] = '0.0.0.0'
    if environ['HBNB_API_PORT'] is None:
        environ['HBNB_API_PORT'] = 5000
    app.run(host=environ['HBNB_API_HOST'],
            port=environ['HBNB_API_PORT'], threaded=True,
            debug=True)
