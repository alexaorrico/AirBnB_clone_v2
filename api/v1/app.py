#!/usr/bin/python3
"""
-------------------------------------------------------------------------------
MODULE NAME: app
-------------------------------------------------------------------------------
"""
from models import storage
from flask import Flask, Blueprint, render_template,jsonify
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def error404(code_error):
    '''return error 404 not found format json'''
    return jsonify(error="Not found"), 404



if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),
        port=getenv("HBNB_API_PORT", 5000),
        threaded=True
    )
