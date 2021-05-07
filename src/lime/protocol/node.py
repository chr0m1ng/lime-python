from identity import Identity

DOMAIN_SEPARATOR = '@'


class Node:
    """Node represents a identity with an instance."""

    def __init__(self, identity: Identity = None, instance: str = None):
        self.identity = identity
        self.instance = instance

    def to_identity(self) -> Identity:
        """Parse a identity into a Node.

        Returns:
            Identity: Return a identity object
        """
        return self.identity

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
        props = possible_node.split(DOMAIN_SEPARATOR)
        if len(props) < 2:
            return None
        name, domain = props
        return Node(name, domain)

    @staticmethod
    def parse(possible_node: str | Identity):
        """Parse a possible node into a Node.

        Args:
            possible_node (str|Identity|Node): possible Node object

        Returns:
            [Node]: Returns a node object
        """
        if isinstance(possible_node, Node):
            return possible_node
        else:
            identity = Identity.parse(possible_node)
            if identity is not None:
                instance = str(possible_node).replace(identity, str())
                return Node(identity, instance)
