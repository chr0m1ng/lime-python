from typing import Any
from .envelope import Envelope
from .reason import Reason


class Command(Envelope):
    """Command representation."""

    def __init__(
        self,
        method: str,
        uri: str = None,
        type_n: str = None,
        resource: Any = None,
        status: str = None,
        reason: Reason = None,
        timeout: bool = None
    ) -> None:
        super().__init__()
        self.method = method
        self.uri = uri
        self.type_n = type_n
        self.resource = resource
        self.status = status
        self.reason = reason
        self.timeout = timeout
