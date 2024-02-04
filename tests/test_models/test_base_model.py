import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    def test_save_method(self):
        model = BaseModel()
        model.save()
        self.assertIsNotNone(model.updated_at)

    def test_delete_method(self):
        model = BaseModel()
        model.save()
        model.delete()
        self.assertIsNone(model.updated_at)


if __name__ == '__main__':
    unittest.main()
