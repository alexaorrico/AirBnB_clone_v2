#!/usr/bin/python3
"""
Create a Blueprint and define it's url_prefix
"""
from .. import models
from flask import Blueprint

storage = models.storage
City, Place = models.city.City, models.place.Place
User, State = models.user.User, models.state.State
Review, Amenity = models.review.Review, models.amenity.Amenity

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

__all__ = [app_views, storage, City, User, Place, State, Review, Amenity]

from .index import *
from .users import *
from .places import *
from .states import *
from .cities import *
from .amenities import *
from .places_reviews import *
from .places_amenities import *
