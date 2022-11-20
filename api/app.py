#!/usr/bin/python3
"""flask sever"""


from flask import jsonify, Flask
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown.appcontext
def downtear(self):
    storage.close()
if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
        app.run(host=host, port=port, threaded=True)
