#!/usr/bin/python3
"""A simple REST API application to print status OK"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """A method to handle closing of application"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
