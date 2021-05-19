from ..serializable import Serializable

NORMALIZED_KEYS = frozenset(('from', 'type'))


class DictToClass(Serializable):
    """Turns a dictionary into a class."""

    def __init__(self, dictionary: dict, class_type: type):
        for key, value in dictionary.items():
            setattr(self, self.__normalize_key(key), value)
        self.__class__ = class_type

    def __normalize_key(self, key):
        if key in NORMALIZED_KEYS:
            key = f'{key}_n'
        return key
