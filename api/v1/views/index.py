"""Index"""
from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def status():
    """returns a JSON"""
    return {"status": "OK"}

@app_views.route('/api/v1/stats')
def class_count():
    """retrieves the number of each objects by type"""
    return {
        "amenities": storage.count("amenities"),
        "cities": storage.count("cities"), 
        "places": storage.count("places"), 
        "reviews": storage.count("reviews"), 
        "states": storage.count("states"), 
        "users": storage.count("users")
        }
