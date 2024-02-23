from flask import Flask
from models import storage
from api.v1.views import app_views

# Create a variable app, instance of Flask
app = Flask(__name__)

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# Declare a method to handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the current SQLAlchemy session."""
    storage.close()

# Inside if __name__ == "__main__":, run your Flask server (variable app)
if __name__ == "__main__":
    # Define host and port based on environment variables or default values
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    
    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
