#!/usr/bin/python3

"""
implement status route
return the status of API
"""


from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint('app_views')
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(self):
    """
    close storage session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
