#!/usr/bin/python3
'''Model blueprint'''
from models import storage
from api.v1.views import app_views
import flask

app = flask.Flask(__name__)
app.register_blueprint(app_views)

@app.route('/', strict_slashes=False)
def index():
    """Hello HBNB!"""
    return ('Hello HBNB!')

@app.teardown_appcontext
def teardown(self):
    '''Method that calls storage.close()'''
    storage.close()

if __name__ == "__main__":
    HBNB_API_HOST = '0.0.0.0'
    HBNB_API_PORT = '5000'
    app.run(debug=True, threaded=True, host=HBNB_API_HOST, port=HBNB_API_PORT)

