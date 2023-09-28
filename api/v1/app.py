#!/usr/bin/python3
"""a functon to get status of API"""
import os
from flask.app import Flask
app = Flask(__name__)
print(dir(app))
from models import storage
from api.v1.views import app_views
app.register_blueprint(app_views)

@app.teardown_appcontext
def handle_teardown(exception):
    """handle @app.teardown_appcontext"""
    storage.close()

if __name__ == "__main__":
    hst = os.getenv('HBNB_API_HOST')
    prt = os.getenv('HBNB_API_PORT')
    if hst and prt:
        app.run(host=hst, port=prt, threaded=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True)
