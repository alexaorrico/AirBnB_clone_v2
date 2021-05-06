#!/usr/bin/python3
'''  flask app  '''

from os import environ
from models import storage
from api.v1.views import app_views
from flask import Flask
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_session(exception):
    ''' removes current Session '''
    storage.close()


if __name__ == '__main__':
    host_address = environ.get('HBNB_API_HOST', '0.0.0.0')
    port_number = environ.get('HBNB_API_PORT', '5000')
    app.run(host=host_address, port=port_number, threaded=True)
