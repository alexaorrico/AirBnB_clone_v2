#!/usr/bin/python3
"""Blueprint instance"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


class Views:
    """TO stop importation Error"""
    from api.v1.views.index import get_status, get_stats
    from api.v1.views.states import state, one_state, del_state, post_state, update_state
    from api.v1.views.amenities import get_amenities, one_amenity, remove_amenity, create_amenity, update_amenity
    from api.v1.views.places import get_places, get_place, delete_place, create_place
    from api.v1.views.cities import get_cities, get_city, delete_city, create_city
    from api.v1.views.users import get_users, get_user, delete_user, create_user, update_user
    from api.v1.views.places_reviews import get_reviews, get_review, delete_review, create_review, update_review
