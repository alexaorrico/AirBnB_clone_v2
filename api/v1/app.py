#!/usr/bin/python3
""" Flask app with cors module   """

from models import storage
from api.v1.views import app_views
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_request(exception=None):
    """Closes the connection when the execution finish"""
    storage.close()


if __name__ == "__main__":
    """ Flask main function """
    my_host = environ.get("HBNB_API_HOST")
    my_port = environ.get("HBNB_API_PORT")
    app.run(host=my_host, port=my_port, threaded=True, debug=True)
