import unittest
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

FileStorage = file_storage.FileStorage
classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(file_storage.get_storage_type() == "db", "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(file_storage.get_storage_type() == "db", "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = storage._FileStorage__objects.copy()
        storage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            storage.new(instance)
            test_dict[instance_key] = instance
            self.assertEqual(test_dict, storage._FileStorage__objects)
        storage._FileStorage__objects = save

    @unittest.skipIf(file_storage.get_storage_type() == "db", "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = storage._FileStorage__objects.copy()
        storage._FileStorage__objects = new_dict
        storage.save()
        storage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        storage.reload()
        for key, value in new_dict.items():
            cls_name, obj_id = key.split(".")
            obj = storage._FileStorage__objects[key]
            self.assertEqual(obj_id, obj.id)
            self.assertEqual(cls_name, obj.__class__.__name__)
            for k, v in value.items():
                if k != "updated_at" and k != "created_at":
                    self.assertEqual(str(getattr(obj, k)), str(v))
                else:
                    obj_datetime = getattr(obj, k).strftime("%Y-%m-%dT%H:%M:%S.%f")
                    self.assertEqual(obj_datetime, v)


if __name__ == "__main__":
    unittest.main()
