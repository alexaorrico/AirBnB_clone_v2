def get(self, cls, id):
        """ retrieves"""
        if cls in classes.values() and id and type(id) == str:
            d_obj = self.all(cls)
            for key, value in d_obj.items():
                if key.split(".")[1] == id:
                    return value
        return None

    def count(self, cls=None):
        """ counts"""
        data = self.all(cls)
        if cls in classes.values():
            data = self.all(cls)
        return len(data)
