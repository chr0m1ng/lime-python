from ..constants import AuthenticationScheme
from .authentication import Authentication


class PlainAuthentication(Authentication):
    """Plain authentication representation."""

    def __init__(self, password: str, **kwargs) -> None:
        super().__init__(AuthenticationScheme.PLAIN, **kwargs)
        self.password = password
