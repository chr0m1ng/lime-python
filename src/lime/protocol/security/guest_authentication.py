from .authentication import Authentication


class GuestAuthentication(Authentication):
    """Guest authentication representation."""

    def __init__(self, scheme: str):  # noqa: WPS612
        self.scheme = scheme
