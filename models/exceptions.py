class BaseModelInvalidObject(Exception):
    """Exception raised for errors in the updating storage
    from BaseModel.

    Attributes:
        object -- the invalid object id.
        message -- explanation of the error
    """

    def __init__(self, objectId,
                 message="Tried to update an object that doesn't\
                    exist in storage",
                 code="-1"):
        """init for exception"""
        self.objectId = objectId
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        """str definition"""
        return ('{} -> {} -> {}'.format(
            self.code,
            self.objectId,
            self.message))


class BaseModelInvalidDataDictionary(Exception):
    """Exception raised for errors in the updating storage
    from BaseModel

    Attributes:
        dictionary -- dictionary which caused the error
        message -- explanation of the error
    """

    def __init__(self, dictionary,
                 message="Tried to update an object without\
                    correct dictionary",
                 code="-2"):
        """init for exception"""
        self.dictionary = dictionary
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        """str definition"""
        return ('{} -> {} -> {}'.format(
            self.code,
            self.dictionary,
            self.message))


class BaseModelMissingAttribute(Exception):
    """Exception raised for errors in the updating storage
    from BaseModel

    Attributes:
        attribute -- attribute which was missing
        message -- explanation of the error
    """

    def __init__(self, attribute,
                 message="Tried to update an object without\
                    correct attributes",
                 code="-3"):
        """init for exception"""
        self.attribute = attribute
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        """str definition"""
        return ('{}'.format(self.attribute))
