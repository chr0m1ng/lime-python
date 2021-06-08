from typing import List

from .envelope import Envelope
from .reason import Reason


class Session(Envelope):
    """Session representation."""

    def __init__(  # noqa: WPS211
        self,
        state: str = None,
        encryption_options: List[str] = None,
        encryption: str = None,
        compression_options: List[str] = None,
        compression: str = None,
        scheme: str = None,
        scheme_options: List[str] = None,
        authentication=None,
        reason: Reason = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.state = state
        self.encryption_options = encryption_options
        self.encryption = encryption
        self.compression_options = compression_options
        self.compression = compression
        self.scheme = scheme
        self.scheme_options = scheme_options
        self.authentication = authentication
        self.reason = reason
