#!/usr/bin/python3
<<<<<<< HEAD
'''
Createw Flask app; and register blueprint app_views to Flask instance app.
'''

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# enable CORS and allow for origins:
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

=======
"""app"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.url_map.strict_slashes = False
>>>>>>> 6a3b9b65fb88b26a94fce1815dc7223dece11944
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
<<<<<<< HEAD
def teardown_engine(exception):
    '''
    Removes current SQLAlchemy Session object after each request.
    '''
    storage.close()


# Error handlers for expected app behavior:
@app.errorhandler(404)
def not_found(error):
    '''
    Return the errmsg `Not Found`.
    '''
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
=======
def tear(self):
    ''' closes storage engine '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    ''' handles 404 error and gives json formatted response '''
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
>>>>>>> 6a3b9b65fb88b26a94fce1815dc7223dece11944
