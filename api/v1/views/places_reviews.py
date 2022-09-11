#!/usr/bin/python3
"""file places_reviews"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
import json

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review(place_id=None):
    """review function"""
    list_of_reviews = []
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    for review in places.reviews:
        list_of_reviews.append(review.to_dict())
    return jsonify(list_of_reviews)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviewid(review_id=None):
    """review id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviewdel(review_id=None):
    """review delete"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
    """
    Create a Review object.
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    body = request.get_json()

    # If the HTTP request body is not valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Traemos place por su "id"
    place = storage.get(Place, place_id)

    # If the place_id is not linked to any Place object, raise a 404 error
    if place is None:
        abort(404)

    # Si el body no tiene la variable "user_id" se imprime el error y su stat
    if "user_id" not in body:
        return (jsonify({'error': 'Missing user_id'}), 400)

    # Usamos el metodo get() de python para obtener el user_id
    user_id = body.get("user_id")
    # creamos un usuario usando el metodo get() que creamos nosotros
    user = storage.get(User, user_id)
    # If the user_id is not linked to any User object, raise a 404 error
    if user is None:
        abort(404)

    # Si el body no tiene la variable "text" se imprime el error y su status
    if "text" not in body:
        return (jsonify({'error': 'Missing text'}), 400)

    # Si se paso "text" y "user_id" se crea el objeto y se guarda en la base de
    # datos Se crea el nuevo objeto pasandole como "kwargs" el diccionario que
    # traemos con la request en "body".
    # Se agrega las "id" al dic "body", ya que en el body de la request
    # solo se mandan los datos de json no estan las id en el body
    body['place_id'] = place_id
    body['user_id'] = user_id

    # Se crea una instancia de la clase Review
    obj = Review(**body)

    storage.new(obj)
    # Se guarda el nuevo objeto dentro del storage
    storage.save()

    # Se devuelve el objeto creado y un status code de 201
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('reviews/review_id', methods=['PUT'], strict_slashes=False)
def reviewput(review_id=None):
    """review put"""
    notAttr = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    body = request.get_json()
    if body is None:
        return jsonify({
            "error": "Not a JSON"
        }), 400
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    for key, value in body.items():
        if key not in notAttr:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
