from ..serializable import Serializable


class Authentication(Serializable):
    """Authentication scheme."""

    def __init__(self, authentication_scheme: str):
        self.scheme = authentication_scheme
