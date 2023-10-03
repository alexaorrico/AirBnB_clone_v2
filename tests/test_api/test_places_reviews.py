# tests/test_places_reviews.py

import unittest
from flask import Flask, json, jsonify
from api.v1.views import app_views
from models import storage, Review, Place, User, City

class TestPlacesReviewsRoute(unittest.TestCase):
    """Test cases for the Places Reviews view."""

    def setUp(self):
        """Set up the test environment."""
        self.app = Flask(__name__)
        app_views.app.config["TESTING"] = True
        self.client = app_views.app.test_client()
        
        # Create a test City, User, Place, and Review
        self.city = City(name="Test City")
        self.user = User(email="user@example.com", password="password")
        self.place = Place(name="Test Place", city_id=self.city.id, user_id=self.user.id)
        self.review = Review(text="Test Review", place_id=self.place.id, user_id=self.user.id)
        self.city.save()
        self.user.save()
        self.place.save()
        self.review.save()

    def tearDown(self):
        """Tear down the test environment."""
        storage.close()

    def test_get_reviews_by_place_route(self):
        """Test the /places/<place_id>/reviews route (GET)."""
        response = self.client.get(f"/api/v1/places/{self.place.id}/reviews")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["text"], "Test Review")

    def test_get_review_route(self):
        """Test the /reviews/<review_id> route (GET)."""
        response = self.client.get(f"/api/v1/reviews/{self.review.id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["text"], "Test Review")

    def test_delete_review_route(self):
        """Test the /reviews/<review_id> route (DELETE)."""
        response = self.client.delete(f"/api/v1/reviews/{self.review.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{}')
        # Verify that the review is deleted
        deleted_review = storage.get(Review, self.review.id)
        self.assertIsNone(deleted_review)

    def test_create_review_route(self):
        """Test the /places/<place_id>/reviews route (POST)."""
        data = {
            "user_id": self.user.id,
            "text": "New Review"
        }
        response = self.client.post(f"/api/v1/places/{self.place.id}/reviews",
                                    data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["text"], "New Review")
        # Verify that the review is created
        new_review = storage.get(Review, data["id"])
        self.assertIsNotNone(new_review)

    def test_update_review_route(self):
        """Test the /reviews/<review_id> route (PUT)."""
        data = {
            "text": "Updated Review"
        }
        response = self.client.put(f"/api/v1/reviews/{self.review.id}",
                                   data=json.dumps(data),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["text"], "Updated Review")
        # Verify that the review is updated
        updated_review = storage.get(Review, self.review.id)
        self.assertEqual(updated_review.text, "Updated Review")

if __name__ == "__main__":
    unittest.main()
