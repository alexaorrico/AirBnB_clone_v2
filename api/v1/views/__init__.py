from flask import Flask
from models import storage
from api.v1.views.places_reviews import bp as places_reviews_bp

app = Flask(__name__)

app.register_blueprint(places_reviews_bp)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the storage on teardown of the Flask application context.
    """
    storage.close()
