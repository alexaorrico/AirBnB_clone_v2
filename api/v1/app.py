#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(excptions):
    """ handle teardown app context"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
