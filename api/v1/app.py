<<<<<<< HEAD
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
=======
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

>>>>>>> master

app = Flask(__name__)
app.register_blueprint(app_views)

<<<<<<< HEAD

@app.errorhandler(404)
def not_found_json_output(exception):
    """
    Returns JSON {'error': 'Not found'}, 404
    when a 404 error occurs
    """
    return {'error': 'Not found'}, 404


@app.teardown_appcontext
def close_db(exception: Exception):
    """
    Calls 'storage.close()'
    """
    storage.close()


if __name__ == "__main__":
    from os import getenv

    HOST = getenv('HBNB_API_HOST')
    PORT = getenv('HBNB_API_PORT')

    app.run(
        HOST if HOST else '0.0.0.0',
        PORT if PORT else 5000,
        threaded=True
    )
=======
@app.teardown_appcontext
def teardown_db(exception):
    """ This module teardown connection to db"""
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port =port, threaded=True)
>>>>>>> master
