#!/usr/bin/python3
"""
script that starts a Flask web application:
"""
from models import storage
from api.v1.views import app_views
from flask import Blueprint, render_template, abort
from flask import Flask


"""register the blueprint app_views
"""
app = Flask(__name__)
app.register_blueprint(app_views)

app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(self):
    """
        method to handle teardown
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
