from abc import ABC
from .envelope import Envelope
from .reason import Reason
from .session_compression import SessionCompression
from .session_encryption import SessionEncryption
from .session_state import SessionState


class Session(ABC, Envelope):
    """Session representation."""

    def __init__(self,
                 state: SessionState = None,
                 encryption_options: list = None,
                 encryption: SessionEncryption = None,
                 compression_options: list = None,
                 compression: SessionCompression() = None,
                 scheme: str = None,
                 authentication=None,
                 reason: Reason = None):

        self.state = state
        self.encryption_options = encryption_options
        self.encryption = encryption
        self.compression_options = compression_options
        self.compression = compression
        self.scheme = scheme
        self.authentication = authentication
        self.reason = reason


class SessionListener(ABC):
    """Session Listener."""

    def on_session(self, command: Session):
        """Handle session received.

        Args:
            command (Session): command to be received
        """
        pass
