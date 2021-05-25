from ..constants import AuthenticationScheme
from .authentication import Authentication


class KeyAuthentication(Authentication):
    """Key authentication representation."""

    def __init__(self, key: str) -> None:
        super().__init__(AuthenticationScheme.KEY)
        self.key = key
