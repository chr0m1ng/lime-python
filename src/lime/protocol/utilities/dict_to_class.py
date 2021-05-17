class DictToClass:
    """Turns a dictionary into a class."""

    def __init__(self, dictionary: dict, class_type: type):
        for key, value in dictionary.items():
            setattr(self, key, value)
        self.__class__ = class_type
