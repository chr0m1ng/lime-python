from ..constants import AuthenticationScheme
from .authentication import Authentication


class PlainAuthentication(Authentication):
    """Plain authentication representation."""

    def __init__(self, password: str) -> None:
        super().__init__(AuthenticationScheme.PLAIN)
        self.password = password
