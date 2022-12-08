def get(self, cls, id):
'''
Retrieve an obj w/class name and id
'''
result = None
try:
objs = self.\_\_session.query(models.classes[cls]).all()
for obj in objs:
if obj.id == id:
result = obj
except BaseException:
pass
return result

    def count(self, cls=None):
        '''
            Count num objects in DBstorage
        '''
        cls_counter = 0

        if cls is not None:
            objs = self.__session.query(models.classes[cls]).all()
            cls_counter = len(objs)
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(models.classes[k]).all()
                    cls_counter += len(objs)
        return cls_counter
