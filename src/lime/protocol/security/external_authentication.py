from .authentication import Authentication


class ExternalAuthentication(Authentication):
    """External authentication representation."""

    def __init__(self, scheme: str, token: str, issuer: str):
        super().__init__(scheme)
        self.token = token
        self.issuer = issuer
