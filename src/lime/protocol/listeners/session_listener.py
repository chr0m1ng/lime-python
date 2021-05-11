from abc import ABC
from ..session import Session


class SessionListener(ABC):
    """Session Listener."""

    def on_session(self, command: Session):
        """Handle session received.

        Args:
            command (Session): command to be received
        """
        pass
