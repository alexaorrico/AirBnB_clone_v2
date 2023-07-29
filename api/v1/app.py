#!/usr/bin/python3
"""A web flask application"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_session(exception):
    """Calls the storage.close()"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Returns a JSON formatted 404 status code response"""
    return make_response(jsonify(error="Not found"), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
