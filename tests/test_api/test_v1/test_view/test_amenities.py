#!/usr/bin/python3
"""
Testing amenities.py file
"""
from api.v1.app import (app)
import flask
import json
from models import storage
from models.amenity import Amenity
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


class TestAmenityView(unittest.TestCase):
    """Test all routes in amenities.py"""

    @classmethod
    def setUpClass(cls):
        """set the flask app in testing mode"""
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"

    def test_getamenities(self):
        """test listing all amenities"""
        amenity_args = {"name": "quokka"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.get('{}/amenities/'.format(self.path),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(amenity_args["name"],
                      [e.get("name") for e in json_format])
        storage.delete(amenity)

    def test_view_one_amenity(self):
        """test retrieving one amenity"""
        amenity_args = {"name": "quokka", "id": "QO2"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.get('{}/amenities/{}'.format(
            self.path, amenity_args["id"]), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), amenity_args["name"])
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        storage.delete(amenity)

    def test_view_one_amenity_wrong(self):
        """the id does not match a amenity"""
        amenity_args = {"name": "quokka", "id": "QO1"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.get('{}/amenities/{}'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_delete_amenity(self):
        """test delete a amenity"""
        amenity_args = {"name": "quokka", "id": "QO"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.delete('{}/amenities/{}/'.format(
            self.path, amenity_args["id"]),
                                   follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("Amenity", amenity_args["id"]))

    def test_delete_amenity_wrong(self):
        """the id does not match a amenity"""
        amenity_args = {"name": "quokka", "id": "QO"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.delete('{}/amenities/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_create_amenity(self):
        """test creating a amenity"""
        amenity_args = {"name": "quokka", "id": "QO"}
        rv = self.app.post('{}/amenities/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(amenity_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), amenity_args["name"])
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        s = storage.get("Amenity", amenity_args["id"])
        self.assertIsNotNone(s)
        storage.delete(s)

    def test_create_amenity_bad_json(self):
        """test creating a amenity with invalid json"""
        amenity_args = {"name": "quokka", "id": "QO"}
        rv = self.app.post('{}/amenities/'.format(self.path),
                           content_type="application/json",
                           data=amenity_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_amenity_no_name(self):
        """test creating a amenity without a name"""
        amenity_args = {"id": "ZA2"}
        rv = self.app.post('{}/amenities/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(amenity_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing name")

    def test_update_amenity_name(self):
        """test updating a amenity"""
        amenity_args = {"name": "quokka", "id": "QO1"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.put('{}/amenities/{}/'.format(self.path, amenity.id),
                          content_type="application/json",
                          data=json.dumps({"name": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), "Z")
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        storage.delete(amenity)

    def test_update_amenity_id(self):
        """test cannot update amenity id"""
        amenity_args = {"name": "quokka", "id": "QO1"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.put('{}/amenities/{}/'.format(self.path, amenity.id),
                          content_type="application/json",
                          data=json.dumps({"id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), amenity_args["name"])
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        storage.delete(amenity)

    def test_update_amenity_bad_json(self):
        """test update with ill formed json"""
        amenity_args = {"name": "quokka", "id": "QO2"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.put('{}/amenities/{}/'.format(self.path, amenity.id),
                          content_type="application/json",
                          data={"id": "Z"},
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(amenity)

    def test_update_amenity_bad_id(self):
        """test update with no matching id"""
        amenity_args = {"name": "quokka", "id": "QO"}
        amenity = Amenity(**amenity_args)
        amenity.save()
        rv = self.app.put('{}/amenities/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)


if __name__ == "__main__":
    unittest.main()
