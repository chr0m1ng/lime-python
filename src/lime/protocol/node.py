DOMAIN_SEPARATOR = '@'
INSTANCE_SEPARATOR = '/'


class Node:
    """Node represents a identity with an instance."""

    def __init__(self, identity=None, instance: str = None):
        self.identity = identity
        self.instance = instance

    def to_identity(self):
        """Parse a identity into a Node.

        Returns:
            Identity: Return a identity object
        """
        return self.identity

    def __eq__(self, otr) -> bool:
        """Compare two Nodes.

        Args:
            otr: Node to be compared with

        Returns:
            bool: Returns if Nodes are equal
        """
        return self.identity == otr.identity and self.instance == otr.instance

    def __str__(self) -> str:
        """Represent Node as a string.

        Returns:
            str: Node as string
        """
        if self.instance is not None:
            return str(self.identity)

        return f'{self.identity}/{self.instance}'

    @staticmethod
    def parse_str(possible_node: str) -> str:
        """Parse a string into a node.

        Args:
            possible_node (str): string node

        Returns:
            str: Node object
        """
        from .identity import Identity  # NOQA WPS433

        props = possible_node.split(DOMAIN_SEPARATOR)
        if len(props) < 2:
            return None
        name, instance_domain = props
        props = instance_domain.split(INSTANCE_SEPARATOR)
        if len(props) == 2:
            domain, instance = props
            return Node(Identity(name, domain), instance)
        return Node(Identity(name, instance_domain))

    @staticmethod
    def parse(possible_node):
        """Parse a possible node into a Node.

        Args:
            possible_node (str|Identity|Node): possible Node object

        Returns:
            [Node]: Returns a node object
        """
        from .identity import Identity  # NOQA WPS433

        if isinstance(possible_node, Node):
            return possible_node
        else:
            identity = Identity.parse(possible_node)
            if identity is not None:
                instance = str(possible_node).replace(str(identity), str())
                return Node(identity, instance)
