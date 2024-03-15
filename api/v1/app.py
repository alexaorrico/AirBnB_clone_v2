#!/bin/usr/python3
""" initializes Flask application """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_db():
    """ closes db """
    return storage.close()

if __name__ == '__main__':
    app_views.run(debug=True, host='0.0.0.0', port='5000')
