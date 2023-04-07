#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import TestBaseModel
from models.place import Place


class TestPlace(TestBaseModel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ """
        new = self.value()
        new.city_id = "7492"
        self.assertEqual(type(new.city_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        new.user_id = "847299"
        self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """ """
        new = self.value()
        new.name = "Monkey D.Luffy"
        self.assertEqual(type(new.name), str)

    def test_description(self):
        """ """
        new = self.value()
        new.description = "The one piece is real"
        self.assertEqual(type(new.description), str)

    def test_number_rooms(self):
        """ """
        new = self.value()
        new.number_rooms = 9
        self.assertEqual(type(new.number_rooms), int)

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        new.number_bathrooms = 8
        self.assertEqual(type(new.number_bathrooms), int)

    def test_max_guest(self):
        """ """
        new = self.value()
        new.max_guest = 3
        self.assertEqual(type(new.max_guest), int)

    def test_price_by_night(self):
        """ """
        new = self.value()
        new.price_by_night = 700
        self.assertEqual(type(new.price_by_night), int)

    def test_latitude(self):
        """ """
        new = self.value()
        new.latitude = 34.55
        self.assertEqual(type(new.latitude), float)

    def test_longitude(self):
        """ """
        new = self.value()
        new.longitude = 749.5
        self.assertEqual(type(new.longitude), float)

    def test_amenity_ids(self):
        """ """
        new = self.value()
        new.amenity_ids = list()
        self.assertEqual(type(new.amenity_ids), list)
