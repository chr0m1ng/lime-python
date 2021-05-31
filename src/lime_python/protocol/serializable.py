import json
from typing import Any
from humps import camelize
from .utilities import DictToClass

PRIVATE_TOKEN = '_'  # noqa: S105
NODE_KEY_TOKEN = '_n'  # noqa: S105


class Serializable:
    """Serializable objects to json."""

    @classmethod
    def from_json(cls: Any, raw_json: dict) -> Any:
        """Deserialize the given json.

        Args:
            raw_json (dict): the json

        Returns:
            Any: the deserialized class
        """
        return DictToClass(raw_json, cls)

    def __str__(self) -> str:
        """Override str representation.

        Returns:
            str: json representation as str
        """
        return json.dumps(self.to_json())

    def __repr__(self) -> str:
        """Representation of the class.

        Returns:
            str: json representation
        """
        return str(self)

    def __eq__(self, obj: object) -> bool:
        """Override equal to compare serializated content.

        Args:
            obj (object): the object to compare

        Returns:
            bool
        """
        return isinstance(obj, Serializable) and \
            self.to_json() == obj.to_json()

    def __hash__(self) -> int:
        """Create a hash based on serializated content.

        Returns:
            int
        """
        return hash(str(self))

    def to_json(self) -> dict:
        """
        Transform class properties to json.

        Returns:
            dict: the class json representation without private properties
        """
        return {
            self.normalize_key(key): self.serialize_value(value)
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
        return camelize(key.replace(NODE_KEY_TOKEN, str()))

    def serialize_value(self, value: Any) -> Any:
        """Serialize a value if it's Serializable.

        Args:
            value (Any): property value

        Returns:
            Any: the serialized property
        """
        return value.to_json() if isinstance(value, Serializable) else value

    def __should_serialize_property(self, key: str, value) -> bool:
        return not key.startswith(PRIVATE_TOKEN) and value is not None
