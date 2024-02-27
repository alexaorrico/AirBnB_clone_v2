# #!/usr/bin/python3
# """
# a new view for State objects that handles all default RESTFul API actions
# """
# from flask import abort, jsonify, request

# from api.v1.views import app_views
# from models import storage
# from models.place import Place
# from models.city import City


# @app_views.route("/cities/<city_id>/places", methods=["GET"],
#                  strict_slashes=False)
# def get_places_of_city(city_id):
#     """Retrieves the list of all Place objects of a city"""
#     city = storage.get(City, str(city_id))
#     if city is None:
#         abort(404)
#     places = [place.to_dict() for place in city.places]
#     return jsonify(places), 200


# @app_views.route("/places/<place_id>", methods=["GET"],
#                  strict_slashes=False)
# def get_places(place_id):
#     """Retrieves the list of all Place objects"""
#     all_places = storage.get("Place", str(place_id))
#     if all_places is None:
#         abort(404)
#     places = [place.to_dict() for place in all_places]
#     return jsonify(places), 200


# @app_views.route("/places/<place_id>", methods=["DELETE"],
#                  strict_slashes=False)
# def delete_place(place_id):
#     """Deletes an Place object"""
#     place = storage.get("Place", str(place_id))
#     if place is None:
#         abort(404)
#     storage.delete(place)
#     storage.save()
#     return ({}), 200


# @app_views.route("/cities/<city_id>/places", methods=["POST"],
#                  strict_slashes=False)
# def create_place(city_id):
#     """Creates an Amenity"""
#     city = storage.get("City", city_id)
#     if city is None:
#         abort(404)
#     dict_ = request.get_json(silent=True)
#     if dict_ is None:
#         abort(400, "Not a JSON")
#     if "user_id" not in dict_:
#         abort(400, "Missing user_id")
#     if "name" not in dict_:
#         abort(400, "Missing name")
#     user = storage.get("User", dict_["user_id"])
#     if user is None:
#         abort(404)
#     place = Place(**dict_)
#     place.save()
#     return jsonify(place.to_dict()), 201


# @app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
# def update_place(amenity_id):
#     """Updates an Place object"""
#     place_obj = storage.get("Place", str(amenity_id))
#     place_dict = request.get_json(silent=True)
#     if place_obj is None:
#         abort(404)
#     if place_dict is None:
#         abort(400, "Not a JSON")
#     for key, val in place_dict.items():
#         if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
#             setattr(place_obj, key, val)
#     place_obj.save()
#     return jsonify(place_obj.to_dict()), 200


# # get the object to be updated by it's id
# # get the dictionary repr of state instance for id=state_id using get_json()
# # check if it's a valid json and return none if it's not
# # iterate the dictionary
# # id, created_at and updated_at should not be available to be set
# # set object attributes based on their keys
