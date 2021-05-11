from .authentication import Authentication


class TransportAuthentication(Authentication):
    """Transport authentication representation."""

    def __init__(self, scheme: str):
        self.scheme = scheme
