import json

PRIVATE_TOKEN = '_'  # noqa: S105
NODE_KEY_TOKEN = '_n'  # noqa: S105


class Serializable:
    """Serializable objects to json."""

    def __str__(self) -> str:
        """Override str representation.

        Returns:
            str: json representation as str
        """
        return json.dumps(self.to_json())

    def to_json(self) -> dict:
        """
        Transform class properties to json.

        Returns:
            dict: the class json representation without private properties
        """
        return {
            self.normalize_key(key): value
            for key, value in self.__dict__.items()  # noqa: WPS110
            if self.__should_serialize_property(key, value)
        }

    def normalize_key(self, key: str) -> str:
        """
        Normalize a class property name.

        Args:
            key (str): property name

        Returns:
            str: the normalized key
        """
        return key.replace(NODE_KEY_TOKEN, str())

    def __should_serialize_property(self, key: str, value) -> bool:
        return not key.startswith(PRIVATE_TOKEN) and value is not None
