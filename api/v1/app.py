#!/usr/bin/python3
'''a script that starts a Flask web application has routes for
hbnb airBnB clone
'''

from api.v1.views import app_views
from models import storage
from flask import Flask
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    '''Tear down seesion: db'''
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
