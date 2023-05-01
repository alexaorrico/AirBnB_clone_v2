#!/usr/bin/python3
'''a script that starts a Flask web application has routes for
hbnb airBnB clone
'''

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    '''Tear down seesion: db'''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''Custom 404 error handler'''
    return make_response(jsonify({"error": "Not found"}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
