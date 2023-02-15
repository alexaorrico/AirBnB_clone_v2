#!/usr/bin/python3
'''Run Flask application
'''
from models import storage
from models import storage


app = Flask(__name__)
'''Flask instance'''
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_flask(exception):
    '''method that handles teardown'''
    storage.close()


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
