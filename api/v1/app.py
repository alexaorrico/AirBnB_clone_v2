<<<<<<< HEAD
from os import getenv

from flask import Flask

from api.v1.views import app_views
from models import storage

=======
#!/usr/bin/python3
"""
Registers Blueprint 'app_views'
from 'api.v1.views' into this script's
app, 'app', then runs 'app'

with
-----------------------------------------
host=HBNB_API_HOST and port=HBNB_API_PORT
-----------------------------------------
with default values being:
----------------------------
host='0.0.0.0' and port=5000
----------------------------
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

>>>>>>> 72c2052882cf43eedee79d8e5c351fe895479708
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ This module teardown connection to db"""
    storage.close()


@app.errorhandler(404)
def not_found_json_output(exception):
    """
    Returns JSON {'error': 'Not found'}, 404
    when a 404 error occurs
    """
    return {'error': 'Not found'}, 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port =port, threaded=True)
