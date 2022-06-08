#!/usr/bin/python3
"""places api"""

from api.v1.views import app_views
from models.engine.db_storage import classes
from models import storage
from flask import jsonify, abort, request

@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"])
def reviews_view(review_id=None, place_id=None):
    if place_id:
        place_obj = storage.get(classes["Place"], place_id)
        if not place_obj:
            abort(404)

        if request.method == "GET":
            review_list = []
            for review in place_obj.reviews:
                review_dict = review.to_dict()
                review_list.append(review_dict)
                
            return jsonify(review_list)
        else:
            request_dict = request.get_json()
            if "text" not in request_dict.keys():
                return jsonify({"error": "Missing text"}), 400

            if "user_id" not in request_dict.keys():
                return jsonify({"error": "Missing user_id"}), 400

            if not storage.get(request_dict.get("user_id")):
                abort(404)
            
            new_review = classes["Place"](text = request_dict["text"], 
                                        place_id = place_id,
                                        user_id = request_dict["user_id"]
                                        )
            new_review.save()

            new_review_dict = new_review.to_dict()
            return jsonify(new_review_dict), 201
    else:
        review_obj = storage.get(classes["Review"], review_id)
        if not review_obj:
            abort(404)

        if request.method == "GET":
            review_dict = review_obj.to_dict()
                
            return jsonify(review_obj)
        elif request.method == "PUT":
            try:
                obj_json = request.get_json()
            except:
                return jsonify({"error": "Not found"}), 400

            for key, value in obj_json.items():
                if key not in ["updated_at", "id", "created_at", "user_id", "place_id"]:
                    setattr(review_obj, key, value)

            review_obj.save()

            review_dict = review_obj.to_dict()
            return jsonify(review_dict), 200
        elif request.method == "DELETE":
            review_obj.delete()
            storage.save()

            return jsonify({})
