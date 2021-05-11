from .constants import SessionCompression, SessionEncryption, SessionState
from .envelope import Envelope
from .reason import Reason


class Session(Envelope):  # noqa: WPS230
    """Session representation."""

    def __init__(
        self,
        state: SessionState = None,
        encryption_options: list = None,
        encryption: SessionEncryption = None,
        compression_options: list = None,
        compression: SessionCompression() = None,
        scheme: str = None,
        authentication=None,
        reason: Reason = None
    ):

        self.state = state
        self.encryption_options = encryption_options
        self.encryption = encryption
        self.compression_options = compression_options
        self.compression = compression
        self.scheme = scheme
        self.authentication = authentication
        self.reason = reason
