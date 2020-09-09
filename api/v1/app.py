from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(obj):
    """ Close the connection in the end of the
    program """
    storage.close()


def handle_bad_request(error):
    """ handler the error in the request and say not found """
    return make_response(jsonify({
        'error': 'Not found'
        }), 404)


app.register_error_handler(404, handle_bad_request)

if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST'),
        port=getenv('HBNB_API_PORT'),
        threaded=True)
