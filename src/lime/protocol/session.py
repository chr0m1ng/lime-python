from typing import List

from .envelope import Envelope
from .reason import Reason


class Session(Envelope):
    """Session representation."""

    def __init__(
        self,
        state: str,
        encryption_options: List[str] = None,
        encryption: str = None,
        compression_options: List[str] = None,
        compression: str = None,
        scheme: str = None,
        authentication=None,
        reason: Reason = None
    ) -> None:
        super().__init__()
        self.state = state
        self.encryption_options = encryption_options
        self.encryption = encryption
        self.compression_options = compression_options
        self.compression = compression
        self.scheme = scheme
        self.authentication = authentication
        self.reason = reason
