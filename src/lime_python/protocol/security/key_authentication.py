from ..constants import AuthenticationScheme
from .authentication import Authentication


class KeyAuthentication(Authentication):
    """Key authentication representation."""

    def __init__(self, key: str = None, **kwargs) -> None:
        super().__init__(AuthenticationScheme.KEY, **kwargs)
        self.key = key
