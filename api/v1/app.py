#!/usr/bin/python3
"""
starts a Flask web application:
web application must be listening on 0.0.0.0, port 5000
"""

from flask import Flask
from models import storage
from api.v1.views import app_view

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db():
    """closes or otherwise deallocates the resource"""
    storage.close()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', threaded=True)
