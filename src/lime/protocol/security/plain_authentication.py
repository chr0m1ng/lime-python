from ..constants import AuthenticationScheme
from .authentication import Authentication


class PlainAuthentication(Authentication):
    """Plain authentication representation."""

    def __init__(self, password: str):
        super().__init__(AuthenticationScheme.PLAIN)
        self.password = password
