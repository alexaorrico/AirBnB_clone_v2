#!/usr/bin/python3
"""App"""


from flask import Flask
from models import storage
from api.v1.views import app_views
import os
host = os.getenv('HBNB_API_HOST')
port = os.getenv('HBNB_API_PORT')


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exit):
    storage.close()


if __name__ == '__main__':
    print(host or '0.0.0.0')
    print(port or 5000)
    app.run(host=(host or '0.0.0.0'),
            port=(port or 5000), threaded=True, debug=True)
