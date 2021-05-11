from .authentication import Authentication


class ExternalAuthentication(Authentication):
    """Plain authentication representation."""

    def __init__(self, scheme: str, password: str):
        super().__init__(scheme)
        self.password = password
