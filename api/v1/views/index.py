#!/usr/bin/python3
"""index view"""
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.get('/status')
def status():
    """display, 'status': 'ok'"""
    return {'status': "ok"}


@app_views.get('/stats')
def stats():
    """retrieves the number of each objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    stats = {}
    for cls in classes:
        stats[cls.__tablename__] = storage.count(cls)

    return stats
