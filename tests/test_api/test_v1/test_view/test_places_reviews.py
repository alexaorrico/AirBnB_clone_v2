#!/usr/bin/python3
"""
Testing reviews.py file
"""
from api.v1.app import (app)
import flask
import json
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import unittest


def getJson(response):
    """
    Extract the json dictionary from a flask Response object

    Argument:
        response: a reponse object from Flask

    Return:
        a dictionary or None or maybe raise an exception
    """
    return json.loads(str(response.get_data(), encoding="utf-8"))


class TestReviewView(unittest.TestCase):
    """Test all routes in reviews.py"""

    @classmethod
    def setUpClass(cls):
        """
        set the flask app in testing mode
        create a state, city, user to test places
        """
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"
        cls.state_args = {"name": "Botswana", "id": "BO"}
        cls.state = State(**cls.state_args)
        cls.state.save()
        cls.city_args = {"name": "Gaborone", "id": "GA",
                         "state_id": cls.state.id}
        cls.city = City(**cls.city_args)
        cls.city.save()
        cls.user_args = {"email": "a@b.com", "password": "1234",
                         "id": "U1"}
        cls.user = User(**cls.user_args)
        cls.user.save()
        cls.place_args = {"name": "cage", "city_id": cls.city.id,
                          "user_id": cls.user.id, "id": "CA"}
        cls.place = Place(**cls.place_args)
        cls.place.save()

    @classmethod
    def tearDownClass(cls):
        storage.delete(cls.state)
        storage.delete(cls.user)

    def test_getreviews(self):
        """test listing all reviews in a place"""
        review_args = {"user_id": self.user.id, "place_id": self.place.id,
                       "text": "This is a great place"}
        review = Review(**review_args)
        review.save()

        rv = self.app.get('{}/places/{}/reviews/'.format(
            self.path, self.place.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(review_args["text"],
                      [e.get("text") for e in json_format])
        self.assertIn(review_args["user_id"],
                      [e.get("user_id") for e in json_format])
        storage.delete(review)

    def test_getreviews_bad_place(self):
        """test listing all reviews with a bad place id"""
        review_args = {"text": "what a cage", "place_id": self.place.id,
                       "user_id": self.user.id}
        review = Review(**review_args)
        review.save()
        rv = self.app.get('{}/places/{}/reviews/'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(review)

    def test_view_one_review(self):
        """test retrieving one review"""
        review_args = {"text": "cool cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.get('{}/reviews/{}/'.format(self.path,
                                                  review_args["id"]),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("text"), review_args["text"])
        self.assertEqual(json_format.get("id"), review_args["id"])
        self.assertEqual(json_format.get("user_id"), review_args["user_id"])
        storage.delete(review)

    def test_view_one_review_wrong(self):
        """the id does not match a review"""
        review_args = {"text": "cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.get('{}/reviews/{}/'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(review)

    def test_delete_review(self):
        """test delete a review"""
        review_args = {"text": "poor cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.delete('{}/reviews/{}/'.format(self.path,
                                                     review_args["id"]),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("Review", review_args["id"]))

    def test_delete_review_wrong(self):
        """the id does not match a review"""
        review_args = {"text": "sad cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.delete('{}/reviews/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(review)

    def test_create_review(self):
        """test creating a review"""
        rv = self.app.get('{}/places/{}/reviews/'.format(self.path,
                                                         self.place.id),
                          follow_redirects=True)
        review_args = {"text": "cage",
                       "user_id": self.user.id, "id": "RCA"}
        rv = self.app.post('{}/places/{}/reviews/'.format(self.path,
                                                          self.place.id),
                           content_type="application/json",
                           data=json.dumps(review_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("text"), review_args["text"])
        self.assertEqual(json_format.get("id"), review_args["id"])
        s = storage.get("Review", review_args["id"])
        self.assertIsNotNone(s)
        self.assertEqual(s.user_id, review_args["user_id"])
        storage.delete(s)

    def test_create_review_bad_json(self):
        """test creating a review with invalid json"""
        review_args = {"text": "cage",
                       "user_id": self.user.id, "id": "RCA"}
        rv = self.app.post('{}/places/{}/reviews/'.format(self.path,
                                                          self.place.id),
                           content_type="application/json",
                           data=review_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_review_no_text(self):
        """test creating a review without a text"""
        review_args = {"user_id": self.user.id, "id": "RCA"}
        rv = self.app.post('{}/places/{}/reviews/'.format(
            self.path, self.place.id),
                           content_type="application/json",
                           data=json.dumps(review_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing text")

    def test_create_review_no_user_id(self):
        """test creating a review without a user_id"""
        review_args = {"text": "cage", "id": "RCA"}
        rv = self.app.post('{}/places/{}/reviews/'.format(
            self.path, self.place.id),
                           content_type="application/json",
                           data=json.dumps(review_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing user_id")

    def test_create_review_bad_user_id(self):
        """test creating a review without a valid user_id"""
        review_args = {"text": "cage", "user_id": "noID", "id": "RCA"}
        rv = self.app.post('{}/places/{}/reviews/'.format(
            self.path, self.place.id),
                           content_type="application/json",
                           data=json.dumps(review_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_create_review_bad_place_id(self):
        """test creating a place with not matching state"""
        review_args = {"text": "cage", "user_id": "noID", "id": "RCA"}
        rv = self.app.post('{}/places /{}/reviews/'.format(
            self.path, "noID"),
                           content_type="application/json",
                           data=json.dumps(review_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_update_review_text(self):
        """test updating a review"""
        review_args = {"text": "strong cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.put('{}/reviews/{}/'.format(self.path, review.id),
                          content_type="application/json",
                          data=json.dumps({"text": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("text"), "Z")
        self.assertEqual(json_format.get("id"), review_args["id"])
        self.assertEqual(json_format.get("user_id"), review_args["user_id"])
        self.assertEqual(json_format.get("place_id"), review_args["place_id"])
        storage.delete(review)

    def test_update_review_id(self):
        """test cannot update review id"""
        review_args = {"text": "cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.put('{}/reviews/{}/'.format(self.path, review.id),
                          content_type="application/json",
                          data=json.dumps({"id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("text"), review_args["text"])
        self.assertEqual(json_format.get("id"), review_args["id"])
        self.assertEqual(json_format.get("place_id"), review_args["place_id"])
        self.assertEqual(json_format.get("user_id"), review_args["user_id"])
        storage.delete(review)

    def test_update_review_place_id(self):
        """test cannot update review place_id"""
        review_args = {"text": "cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.put('{}/reviews/{}/'.format(self.path, review.id),
                          content_type="application/json",
                          data=json.dumps({"place_id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("text"), review_args["text"])
        self.assertEqual(json_format.get("id"), review_args["id"])
        self.assertEqual(json_format.get("place_id"), review_args["place_id"])
        self.assertEqual(json_format.get("user_id"), review_args["user_id"])
        storage.delete(review)

    def test_update_review_user_id(self):
        """test cannot update review user_id"""
        review_args = {"text": "cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.put('{}/reviews/{}/'.format(self.path, review.id),
                          content_type="application/json",
                          data=json.dumps({"user_id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("text"), review_args["text"])
        self.assertEqual(json_format.get("id"), review_args["id"])
        self.assertEqual(json_format.get("place_id"), review_args["place_id"])
        self.assertEqual(json_format.get("user_id"), review_args["user_id"])
        storage.delete(review)

    def test_update_review_bad_json(self):
        """test update with ill formed json"""
        review_args = {"text": "cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.put('{}/reviews/{}/'.format(self.path, review.id),
                          content_type="application/json",
                          data={"id": "Z"},
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(review)

    def test_update_place_bad_id(self):
        """test update with no matching id"""
        review_args = {"text": "cage", "place_id": self.place.id,
                       "user_id": self.user.id, "id": "RCA"}
        review = Review(**review_args)
        review.save()
        rv = self.app.put('{}/reviews/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"text": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(review)


if __name__ == "__main__":
    unittest.main()
