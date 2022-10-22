#!/usr/bin/python3
'''
app setup for Airbnb_Clone_v3
'''
from flask import Flask, render_template, make_response, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    storage.close()


if __name__ == "__main__":
    apiHost = getenv("HBNB_API_HOST", default="0.0.0.0")
    apiPort = getenv("HBNB_API_PORT", default=5000)
    app.run(host=apiHost, port=int(apiPort), threaded=True)
