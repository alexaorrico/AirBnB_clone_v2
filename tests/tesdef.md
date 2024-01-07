@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get properly retrieves objects from database"""
        states = models.storage.all(State).values()
        getCheck = None
        if len(states) > 0:
            getCheck = models.storage.get(State, list(states)[0].id)
            self.assertIn(getCheck, states)
        self.assertEqual(getCheck, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count properly counts objects in database"""
        length = len(models.storage.all(State).values())
        self.assertEqual(models.storage.count(State), length)
        length = len(models.storage.all().values())
        self.assertEqual(models.storage.count(), length)


