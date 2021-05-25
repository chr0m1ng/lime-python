from .constants import CommonConstants


class Node:
    """Node represents a identity with an instance."""

    def __init__(self, identity=None, instance: str = None) -> None:
        self.identity = identity
        self.instance = instance

    def to_identity(self):
        """Parse a identity into a Node.

        Returns:
            Identity: Return a identity object
        """
        return self.identity

    def __eq__(self, other) -> bool:
        """Override equality comparision.

        Args:
            other (any): other object

        Returns:
            bool: true if objects are equal.
        """
        return self.identity == other.identity \
            and self.instance == other.instance

    def __str__(self) -> str:
        """Represent Node as a string.

        Returns:
            str: Node as string
        """
        if self.instance is None:
            return str(self.identity)

        return f'{self.identity}/{self.instance}'

    @staticmethod
    def parse_str(possible_node: str):
        """Parse a string into a node.

        Args:
            possible_node (str): string node

        Returns:
            Node: Node object
        """
        from .identity import Identity  # noqa: WPS433

        props = possible_node.split(CommonConstants.DOMAIN_SEPARATOR)
        if len(props) < 2:
            return None
        name, instance_domain = props
        props = instance_domain.split(CommonConstants.INSTANCE_SEPARATOR)
        if len(props) == 2:
            domain, instance = props
            return Node(Identity(name, domain), instance)
        return Node(Identity(name, instance_domain))

    @staticmethod
    def parse(possible_node):
        """Parse a possible node into a Node.

        Args:
            possible_node (str | Identity| Node): possible Node object

        Returns:
            Node: Returns a node object
        """
        from .identity import Identity  # noqa: WPS433

        if isinstance(possible_node, Node):
            return possible_node
        elif isinstance(possible_node, Identity):
            return Node(possible_node)

        return Node.parse_str(possible_node)
