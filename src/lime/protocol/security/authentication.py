from ..serializable import Serializable


class Authentication(Serializable):
    """Authentication scheme."""

    def __init__(self, scheme: str) -> None:
        self.scheme = scheme
