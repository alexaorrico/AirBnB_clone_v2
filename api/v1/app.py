#!/usr/bin/python3
"""modeule for app"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    """teardown func"""
    storage.close()


if __name__ == '__main__':
    """main funcc"""
    host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    port = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)
