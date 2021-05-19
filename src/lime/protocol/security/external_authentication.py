from ..constants import AuthenticationScheme
from .authentication import Authentication


class ExternalAuthentication(Authentication):
    """External authentication representation."""

    def __init__(self, token: str, issuer: str) -> None:
        super().__init__(AuthenticationScheme.EXTERNAL)
        self.token = token
        self.issuer = issuer
