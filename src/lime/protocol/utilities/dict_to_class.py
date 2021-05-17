class DictToClass:
    """Turns a dictionary into a class."""

    def __init__(self, dictionary, class_type):
        for key, value in dictionary.items():
            setattr(self, key, value)
        self.__class__ = class_type
