from ..constants import AuthenticationScheme
from .authentication import Authentication


class GuestAuthentication(Authentication):
    """Guest authentication representation."""

    def __init__(self, **kwargs) -> None:
        super().__init__(AuthenticationScheme.GUEST, **kwargs)
