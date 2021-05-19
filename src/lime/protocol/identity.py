from .constants import CommonConstants


class Identity:
    """Represents an identity in a domain."""

    def __init__(self, name: str = None, domain: str = None) -> None:
        self.name = name
        self.domain = domain

    def __str__(self) -> str:
        """Override to str to reprensent a Identity.

        Returns:
            str: the str representation
        """
        return f'{self.name}@{self.domain}'

    def __eq__(self, other) -> bool:
        """Override equality comparision.

        Args:
            other (any): other object

        Returns:
            bool: true if objects are equal.
        """
        return self.name == other.name and self.domain == other.domain

    @staticmethod
    def parse_str(possible_identity: str):  # noqa: F821
        """Parse a str into a Identity.

        Args:
            possible_identity (str): the str to be parsed

        Returns:
            Identity: the created Identity
        """
        props = possible_identity.split(CommonConstants.DOMAIN_SEPARATOR)
        if len(props) < 2:
            return None
        name, domain = props
        return Identity(
            name,
            domain.split(CommonConstants.INSTANCE_SEPARATOR)[0]
        )

    @staticmethod
    def parse(possible_identity: str):
        """Parse a str | Identity | Node to a Identity.

        Args:
            possible_identity (str | Identity | Node): the value to be parsed

        Returns:
            Identity: the created Identity
        """  # noqa: DAR103
        from .node import Node  # noqa: WPS433

        if (isinstance(possible_identity, Identity)):
            return possible_identity
        elif (isinstance(possible_identity, Node)):
            return possible_identity.identity

        return Identity.parse_str(possible_identity)
