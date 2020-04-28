#!/usr/bin/python3
"""Create a basics routes and register the blueprint
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host='0.0.0.0', port=5000, threaded=True)
