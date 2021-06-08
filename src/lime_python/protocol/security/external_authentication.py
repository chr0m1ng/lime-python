from ..constants import AuthenticationScheme
from .authentication import Authentication


class ExternalAuthentication(Authentication):
    """External authentication representation."""

    def __init__(
        self,
        token: str = None,
        issuer: str = None,
        **kwargs
    ) -> None:
        super().__init__(AuthenticationScheme.EXTERNAL, **kwargs)
        self.token = token
        self.issuer = issuer
