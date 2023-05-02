#!/usr/bin/python3
"""
Testing places_amenities.py file
"""
from api.v1.app import (app)
import flask
import json
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
import os
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


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
class TestPlaceAmenityView(unittest.TestCase):
    """Test all routes in places_amenities.py"""

    @classmethod
    def setUpClass(cls):
        """
        set the flask app in testing mode
        create a state, city, user, place to test place amenities
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
        cls.amenity_args = {"name": "quokka"}
        cls.amenity = Amenity(**cls.amenity_args)
        cls.amenity.save()
        cls.place.amenities.append(cls.amenity)
        cls.place.save()

    @classmethod
    def tearDownClass(cls):
        storage.delete(cls.state)
        storage.delete(cls.user)
        # storage.delete(cls.amenity)

    def test_get_amenities(self):
        """test listing all amenities in a place"""
        rv = self.app.get('{}/places/{}/amenities/'.format(
            self.path, self.place.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(self.amenity_args["name"],
                      [e.get("name") for e in json_format])
        self.assertIn(self.amenity.id,
                      [e.get("id") for e in json_format])

    def test_get_amenities_bad_place(self):
        """test listing all amenities with a bad place id"""
        rv = self.app.get('{}/places/{}/amenities/'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_delete_amenity_in_place(self):
        """test remove an amenity from a place"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        self.place.amenities.append(amenity)
        amenity.save()
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, "BA"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format, {})
        self.assertIsNotNone(storage.get("Amenity", amenity.id))
        storage.delete(amenity)

    def test_delete_amenity_wrong_place(self):
        """the id does not match a place"""
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, "noID", self.amenity.id),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_delete_amenity_wrong_amenity(self):
        """the id does not match an amenity"""
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_delete_amenity_not_in_place(self):
        """test remove an amenity from a place without this amenity"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        # self.place.save()
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, amenity.id),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_link_amenity_place(self):
        """test linking an amenity to a place"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, amenity.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), amenity_args["name"])
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        self.assertIn(self.amenity.id,
                      [a.id for a in storage.get("Place",
                                                 self.place.id).amenities])
        storage.delete(amenity)

    def test_link_amenity_already_in_place(self):
        """test linking an amenity already in place"""
        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, self.amenity.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), self.amenity_args["name"])
        self.assertEqual(json_format.get("id"), self.amenity.id)
        self.assertIn(self.amenity.id,
                      [a.id for a in storage.get("Place",
                                                 self.place.id).amenities])

    def test_link_amenity_bad_place(self):
        """test linking an amenity to a non existing place"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, "noID", amenity.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_link_bad_amenity_place(self):
        """test linking a non existing amenity to a place"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db', "db")
class TestPlaceAmenityViewFS(unittest.TestCase):
    """Test all routes in places_amenities.py"""

    @classmethod
    def setUpClass(cls):
        """
        set the flask app in testing mode
        create a state, city, user, place to test place amenities
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
        cls.amenity_args = {"name": "quokka"}
        cls.amenity = Amenity(**cls.amenity_args)
        cls.amenity.save()
        cls.place.amenities_id.append(cls.amenity.id)
        cls.place.save()

    @classmethod
    def tearDownClass(cls):
        storage.delete(cls.state)
        storage.delete(cls.user)
        # storage.delete(cls.amenity)

    def test_get_amenities(self):
        """test listing all amenities in a place"""
        rv = self.app.get('{}/places/{}/amenities/'.format(
            self.path, self.place.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(self.amenity_args["name"],
                      [e.get("name") for e in json_format])
        self.assertIn(self.amenity.id,
                      [e.get("id") for e in json_format])

    def test_get_amenities_bad_place(self):
        """test listing all amenities with a bad place id"""
        rv = self.app.get('{}/places/{}/amenities/'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_delete_amenity_in_place(self):
        """test remove an amenity from a place"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        self.place.amenities_id.append(amenity.id)
        storage.new(self.place)
        amenity.save()
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, "BA"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format, {})
        self.assertIsNotNone(storage.get("Amenity", amenity.id))
        storage.delete(amenity)

    def test_delete_amenity_wrong_place(self):
        """the id does not match a place"""
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, "noID", self.amenity.id),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_delete_amenity_wrong_amenity(self):
        """the id does not match an amenity"""
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_delete_amenity_not_in_place(self):
        """test remove an amenity from a place without this amenity"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        # self.place.save()
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, amenity.id),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_link_amenity_place(self):
        """test linking an amenity to a place"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, amenity.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), amenity_args["name"])
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        self.assertIn(self.amenity.id,
                      [a.id for a in storage.get("Place",
                                                 self.place.id).amenities])
        storage.delete(amenity)

    def test_link_amenity_already_in_place(self):
        """test linking an amenity already in place"""
        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, self.amenity.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), self.amenity_args["name"])
        self.assertEqual(json_format.get("id"), self.amenity.id)
        self.assertIn(self.amenity.id,
                      [a.id for a in storage.get("Place",
                                                 self.place.id).amenities])

    def test_link_amenity_bad_place(self):
        """test linking an amenity to a non existing place"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, "noID", amenity.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_link_bad_amenity_place(self):
        """test linking a non existing amenity to a place"""
        amenity_args = {"name": "bear", "id": "BA"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)


if __name__ == "__main__":
    unittest.main()
