from humps import decamelize

NORMALIZED_KEYS = frozenset(('from', 'type'))


class DictToClass:
    """Turns a dictionary into a class."""

    def __init__(self, dictionary: dict, class_type: type) -> None:
        for key, value in dictionary.items():
            setattr(self, self.__normalize_key(key), value)
        self.__class__ = class_type

    def __normalize_key(self, key) -> str:
        key = decamelize(key)
        if key in NORMALIZED_KEYS:
            key = f'{key}_n'
        return key
