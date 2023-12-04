class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test the get method in FileStorage"""
        storage = FileStorage()
        obj = User()
        storage.new(obj)
        storage.save()

        # Test when the object is found
        retrieved_obj = storage.get(User, obj.id)
        self.assertEqual(retrieved_obj, obj)

        # Test when the object is not found
        non_existent_obj = storage.get(User, 'nonexistent_id')
        self.assertIsNone(non_existent_obj)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_all(self):
        """Test the count method in FileStorage with all classes"""
        storage = FileStorage()
        count = storage.count()
        self.assertEqual(count, len(storage.all()))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_specific_class(self):
        """Test the count method in FileStorage with a specific class"""
        storage = FileStorage()
        obj1 = User()
        obj2 = User()
        storage.new(obj1)
        storage.new(obj2)
        storage.save()

        count = storage.count(User)
        self.assertEqual(count, 2)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_nonexistent_class(self):
        """Test the count method in FileStorage with a nonexistent class"""
        storage = FileStorage()
        count = storage.count(NonExistentClass)
        self.assertEqual(count, 0)
