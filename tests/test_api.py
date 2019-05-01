#!/usr/bin/python3
"""Test for Api call"""
from models.base_model import Base
from models import storage
from api.v1.app import app
import json
import unittest
import os
import subprocess


class AirbnbTestCase(unittest.TestCase):

    __engine = None
    __app = None

    @classmethod
    def setUpClass(cls):
        """setup the class for testing if storage type is db

        """
        if os.getenv("HBNB_TYPE_STORAGE") == "db"\
                and os.getenv("HBNB_ENV") == "test":
            with open("tests/100-dump.sql", "r") as f:
                cmd = ["mysql", "-uroot", "-pdocker"]
                proc = subprocess.Popen(
                    cmd,
                    stdin=f,
                    stderr=subprocess.DEVNULL
                )
                err, out = proc.communicate()
        cls.__app = app.test_client()

    def test_server_status(self):
        """Test if Status of Api returns a json"""
        with self.__app as a:
            resp = a.get("/api/v1/status")
            self.assertTrue(resp.get_json(silent=True))

    def test_server_status_msg(self):
        """Test if Status of Api returns a json returns
        expected data
        """
        with self.__app as a:
            resp = a.get("/api/v1/status")
            msg = resp.get_json()
            self.assertEqual(msg["status"], "OK")

    def test_some_stats(self):
        """Test if the responce data is json"""
        with self.__app as a:
            resp = a.get("/api/v1/stats")
            self.assertTrue(resp.get_json(silent=True))

    def test_some_stats_count(self):
        """Test the count method for FileStorage and the API call to stats
        The responce message is also tested that the format matches
        the expected specs.
        """
        with open("file.json", encoding="utf-8") as f:
            sample_a = {
                "amenities": storage.count("Amenity"),
                "cities": storage.count("City"),
                "places": storage.count("Place"),
                "reviews": storage.count("Review"),
                "states": storage.count("State"),
                "users": storage.count("User")
            }
        with self.__app as a:
            resp = a.get("/api/v1/stats")
            sample_b = resp.get_json()
            self.assertEqual(sample_a, sample_b)
