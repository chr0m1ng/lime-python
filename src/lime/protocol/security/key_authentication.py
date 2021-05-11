from .authentication import Authentication


class ExternalAuthentication(Authentication):
    """Key authentication representation."""

    def __init__(self, scheme: str, key: str):
        super().__init__(scheme)
        self.key = key
