import unittest
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):

    def test_create_with_dict(self):
        my_dict = {
            'id': '2eec9dfe-4337-401b-a6d6-5c03bb7a3fdd',
            'created_at': '2024-02-05T02:27:49.434934',
            'updated_at': '2024-02-05T02:27:49.434934'
        }
        inst = BaseModel(**my_dict)
        self.assertIsInstance(inst, BaseModel)
        self.assertEqual(inst.id, '2eec9dfe-4337-401b-a6d6-5c03bb7a3fdd')
        self.assertEqual(inst.created_at, datetime(2024, 2, 5, 2, 27, 49, 434934))
        self.assertEqual(inst.updated_at, datetime(2024, 2, 5, 2, 27, 49, 434934))

    def test_create_with_dict_extra_attributes(self):
        my_dict = {
            'id': '2eec9dfe-4337-401b-a6d6-5c03bb7a3fdd',
            'created_at': '2024-02-05T02:27:49.434934',
            'updated_at': '2024-02-05T02:27:49.434934',
            'extra_attr': 'extra_value'
        }
        inst = BaseModel(**my_dict)
        self.assertIsInstance(inst, BaseModel)
        self.assertEqual(inst.id, '2eec9dfe-4337-401b-a6d6-5c03bb7a3fdd')
        self.assertEqual(inst.created_at, datetime(2024, 2, 5, 2, 27, 49, 434934))
        self.assertEqual(inst.updated_at, datetime(2024, 2, 5, 2, 27, 49, 434934))

    def test_create_with_dict_missing_attributes(self):
        my_dict = {
            'id': '2eec9dfe-4337-401b-a6d6-5c03bb7a3fdd',
            'created_at': '2024-02-05T02:27:49.434934'
        }
        inst = BaseModel(**my_dict)
        self.assertIsInstance(inst, BaseModel)
        self.assertEqual(inst.id, '2eec9dfe-4337-401b-a6d6-5c03bb7a3fdd')
        self.assertEqual(inst.created_at, datetime(2024, 2, 5, 2, 27, 49, 434934))
        self.assertIsNotNone(inst.updated_at)

    def test_to_dict(self):
        inst = BaseModel()
        inst_dict = inst.to_dict()
        self.assertIsInstance(inst_dict, dict)
        self.assertEqual(inst_dict['id'], inst.id)
        self.assertEqual(inst_dict['created_at'], inst.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f'))
        self.assertEqual(inst_dict['updated_at'], inst.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f'))

    def test_datetime_attributes(self):
        inst1 = BaseModel()
        inst2 = BaseModel()
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_pep8_conformance(self):
        style_checker = pep8.StyleGuide()
        result = style_checker.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0)

if __name__ == '__main__':
    unittest.main()
