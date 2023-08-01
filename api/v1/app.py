#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

# register blue print app_views
app.register_blueprint(app_views)


# Declare a method to handle @teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_db(exception):
    """
     Teardown the database after each request.

     This function is registered to Flask's teardown_appcontext decorator.
     It closes the database connection after each request.

     :param exception: The exception object, if any.
    """
    storage.close()


if __name__ == "__main__":
    import os

    # get hist and ports
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    # run flask app with environment variables and options
    app.run(host=host, port=port, threaded=True)
