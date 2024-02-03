#!/usr/bin/python3
'''api main app run'''


from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    '''closes storage after done'''
    storage.close()


@app.errorhandler(404)
def er_404(error):
    '''response for 404'''
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', 5000)
    app.run(host=host, port=int(port), threaded=True, debug=1)
