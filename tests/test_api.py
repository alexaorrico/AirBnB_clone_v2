#!/usr/bin/python3
"""Defines unittests for api/."""
import os
import json
import subprocess
import unittest
from models import storage
from models.base_model import Base
from api.v1.app import app


class HolbertonBnBTestCase(unittest.TestCase):
    """Unittests for testing the HolbertonBnB API."""

    __app = None

    @classmethod
    def setUpClass(cls):
        """Setup the class for testing, if testing DBStorage."""
        if (os.getenv("HBNB_TYPE_STORAGE") == "db" and
                os.getenv("HBNB_ENV") == "test"):
            with open("tests/100-dump.sql", "r") as f:
                cmd = ["mysql", "-uroot", "-pdocker"]
                proc = subprocess.Popen(
                    cmd,
                    stdin=f,
                    stderr=subprocess.DEVNULL
                )
                err, out = proc.communicate()
        cls.__app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Drop DBStorage metadata before finishing."""
        if (os.getenv("HBNB_TYPE_STORAGE") == "db"):
            Base.metadata.drop_all(storage._DBStorage__engine)

    def test_server_status(self):
        """Test if /status route returns JSON."""
        with self.__app as a:
            resp = a.get("/api/v1/status")
            self.assertTrue(resp.get_json(silent=True))

    def test_server_status_msg(self):
        """Test if /status route returns expected data."""
        with self.__app as a:
            resp = a.get("/api/v1/status")
            msg = resp.get_json()
            self.assertEqual(msg["status"], "OK")

    def test_stats(self):
        """Test if the /stats route returns JSON."""
        with self.__app as a:
            resp = a.get("/api/v1/stats")
            self.assertTrue(resp.get_json(silent=True))

    def test_stats_data(self):
        """Test the count method for the /stats route.

        Additionally tests format of response JSON object.
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

    @unittest.skip("Awaiting merge.")
    def test_states_get(self):
        """Test GET method on /states route."""
        with self.__app as a:
            resp = a.get("/api/v1/states")
            msg = resp.get_json()
            self.assertEqual(msg, storage.all("State"))
