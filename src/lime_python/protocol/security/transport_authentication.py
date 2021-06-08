from ..constants import AuthenticationScheme
from .authentication import Authentication


class TransportAuthentication(Authentication):
    """Transport authentication representation."""

    def __init__(self, **kwargs) -> None:
        super().__init__(AuthenticationScheme.TRANSPORT, **kwargs)
