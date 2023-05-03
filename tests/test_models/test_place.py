from datetime import datetime
from models import *
# from models.place import PlaceAmenity
import os
import unittest


class Test_PlaceModel(unittest.TestCase):
    """
    Test the place model class
    """
    @classmethod
    def setUpClass(cls):
        """create necessary dependent objects"""
        test_user = {'id': "001",
                     'email': "you@g.com",
                     'password': "1234",
                     'first_name': "TEST",
                     'last_name': "REVIEW"}
        cls.user = User(test_user)
        cls.user.save()
        test_state = {'id': "002",
                      'created_at': datetime(2017, 2, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR CITY"}
        cls.state = State(test_state)
        cls.state.save()
        test_city = {'id': "003",
                     'name': "CITY SET UP",
                     'state_id': "002"}
        cls.city = City(test_city)
        cls.city.save()

    @classmethod
    def tearDownClass(cls):
        storage.delete(cls.state)
        storage.delete(cls.user)

    def test_simple_initialization(self):
        """initialization without arguments"""
        model = Place()
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))

    def test_var_initialization(self):
        """Check default type"""
        test_place = {'id': "003",
                      'city_id': "003",
                      'user_id': "001",
                      'name': "TEST REVIEW",
                      'description': "blah blah",
                      'number_rooms': 4,
                      'number_bathrooms': 2,
                      'max_guest': 4,
                      'price_by_night': 23,
                      'latitude': 45.5,
                      'longitude': 23.4}
        model = Place(test_place)
        self.assertEqual(model.id, test_place["id"])
        self.assertEqual(model.city_id, test_place["city_id"])
        self.assertEqual(model.user_id, test_place["user_id"])
        self.assertEqual(model.name, test_place["name"])
        self.assertEqual(model.description, test_place["description"])
        self.assertEqual(model.number_rooms, test_place["number_rooms"])
        self.assertEqual(model.number_bathrooms,
                         test_place["number_bathrooms"])
        self.assertEqual(model.max_guest, test_place["max_guest"])
        self.assertEqual(model.price_by_night, test_place["price_by_night"])
        self.assertEqual(model.latitude, test_place["latitude"])
        self.assertEqual(model.longitude, test_place["longitude"])

    def test_date_format(self):
        """test the date has the right type"""
        model = Place()
        self.assertIsInstance(model.created_at, datetime)

    def test_delete(self):
        """test the deletion of a city"""
        test_place = {'name': "test_1",
                      'city_id': "003",
                      'user_id': "001"
                      }
        model = Place(**test_place)
        model.save()
        self.assertIn(model.id, storage.all("Place").keys())
        storage.delete(model)
        self.assertIsNone(storage.get("Place", model.id))

    def test_all_place(self):
        """test querying all places"""
        length = storage.count("Place")
        test_place = {'city_id': "003",
                      'user_id': "001"
                      }
        a = Place(**test_place)
        a.name = "test_a"
        b = Place(**test_place)
        b.name = "test_b"
        a.save()
        b.save()
        all_cities = storage.all("Place")
        self.assertIn(a.id, all_cities.keys())
        self.assertIn(b.id, all_cities.keys())
        self.assertEqual(storage.count("Place"), length + 2)
        storage.delete(a)
        storage.delete(b)

    def test_get_place(self):
        """test getting an amenity"""
        test_place = {'name': "test_get",
                      'city_id': "003",
                      'user_id': "001"
                      }
        a = Place(**test_place)
        id_a = a.id
        a.save()
        res = storage.get("Place", id_a)
        self.assertEqual(a.name, res.name)
        self.assertEqual(a.created_at.year, res.created_at.year)
        self.assertEqual(a.created_at.month, res.created_at.month)
        self.assertEqual(a.created_at.day, res.created_at.day)
        self.assertEqual(a.created_at.hour, res.created_at.hour)
        self.assertEqual(a.created_at.minute, res.created_at.minute)
        self.assertEqual(a.created_at.second, res.created_at.second)
        storage.delete(a)

    def test_save(self):
        """saving the object to storage"""
        test_args = {'id': "003",
                     'city_id': "003",
                     'user_id': "001",
                     'name': "TEST REVIEW",
                     'description': "blah blah",
                     'number_rooms': 4,
                     'number_bathrooms': 2,
                     'max_guest': 4,
                     'price_by_night': 23,
                     'latitude': 45.5,
                     'longitude': 23.4}
        place = Place(**test_args)
        place.save()
        all_places = storage.all("Place")
        self.assertIn(test_args['id'], all_places.keys())
        obj = storage.get("Place", test_args['id'])
        self.assertEqual(obj.name, test_args['name'])
        self.assertEqual(obj.created_at.hour, place.created_at.hour)
        storage.delete(place)


# @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
# class Test_PlaceAmenityModel(unittest.TestCase):
#     """
#     Test the place amenity model class
#     """

#     def test_save(self):
#         """creates and save a PlaceAmenity object"""
#         test_user = {'id': "002",
#                      'email': "you@g.com",
#                      'password': "1234",
#                      'first_name': "TEST",
#                      'last_name': "REVIEW"}
#         user = User(**test_user)
#         test_state = {'id': "001",
#                       'created_at': datetime(2017, 2, 12, 00,
#                                              31, 55, 331997),
#                       'name': "TEST STATE FOR CITY"}
#         state = State(**test_state)
#         test_city = {'id': "005",
#                      'name': "CITY SET UP",
#                      'state_id': "001"}
#         city = City(**test_city)
#         test_place = {'id': "002",
#                       'city_id': "005",
#                       'user_id': "002",
#                       'name': "TEST REVIEW",
#                       'description': "blah blah",
#                       'number_rooms': 4,
#                       'number_bathrooms': 2,
#                       'max_guest': 4,
#                       'price_by_night': 23,
#                       'latitude': 45.5,
#                       'longitude': 23.4}
#         place = Place(**test_place)
#         test_amenity = {'id': "010",
#                         'name': "TEST place_amenities"}
#         amenity = Amenity(**test_amenity)
#         pla = PlaceAmenity(place_id="002", amenity_id="010")
#         user.save()
#         state.save()
#         city.save()
#         place.save()
#         amenity.save()
#         storage._DBStorage__session.add(pla)
#         tmp = storage._DBStorage__session.query(PlaceAmenity).one()
#         storage._DBStorage__session.delete(tmp)
        # storage.delete(amenity) ???, foreign key constraint on empty set
        # storage.delete(place)
        # storage.delete(user)
        # storage.delete(state)


if __name__ == "__main__":
    unittest.main()
