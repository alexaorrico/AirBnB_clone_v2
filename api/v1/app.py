#!/usr/bin/python3
"""starts a flask app for our api"""

from flask import Flask
from models import storage
import sys
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear():
    return storage.close()


value_host = getattr(sys.modules[__name__], 'HBNB_API_HOST', None)
value_port = getattr(sys.modules[__name__], 'HBNB_API_PORT', None)
if value_host is not None:
    host = value_host
else:
    host = '0.0.0.0'

if value_port is not None:
    port = value_port
else:
    port = 5000

if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
