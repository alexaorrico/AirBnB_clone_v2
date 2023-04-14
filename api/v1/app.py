#!/usr/bin/python3
'''
create app
'''


from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(code):
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(os.environ.get('HBNB_API_HOST', '0.0.0.0'),
            os.environ.get('HBNB_API_PORT', 5000), threaded=True)
