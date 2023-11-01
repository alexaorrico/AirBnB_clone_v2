#!/usr/bin/python3
"""blueprint"""

from flask import Blueprint
from .. import models

Review, Amenity = models.review.Review, models.amenity.Amenity
City, Place = models.city.City, models.place.Place
storage = models.storage
User, State = models.user.User, models.state.State

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from .amenities import *
from .cities import *
from .index import *
from .places import *
from .states import *
from .places_amenities import *
from .places_reviews import *
from .users import *
