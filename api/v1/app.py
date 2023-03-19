#!/usr/bin/python3
""" flask api module """
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_404(e):
    """ handler for 404 error
    return a machine friendly response
    """
    return {"error": "Not found"}, 404


@app.errorhandler(400)
def error_400(e):
    """ handler for 400 error
    return a machine friendly response
    """
    return {"error": "{}".format(e.description)}, 400


@app.teardown_appcontext
def storage_close(error):
    """ Close the database when app fails
    avoiding to save any change potencially
    harmful
    """
    storage.close()


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=getenv('HBNB_API_PORT', '5000'),
        debug=True,
        threaded=True
    )
