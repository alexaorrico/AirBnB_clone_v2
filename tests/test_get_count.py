def get(self, cls, id):
        """retrieve an object from the database by class and id"""
        return self.all(cls).get(cls.__name__ + '.' + id)

    def count(self, cls=None):
        """count the number of objects in the database"""
        if cls:
            return len(self.all(cls))
        else:
            return sum(len(self.all(c)) for c in classes.values())
