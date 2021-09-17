#!/usr/bin/python3
"""start the flask"""

import os
from flask import Blueprint, render_template, abort
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    storage.close()

if __name__ == "__main__":
    make_h = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    make_p = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host=make_h, port=int(make_p), threaded=True)
