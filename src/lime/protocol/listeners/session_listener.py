from abc import ABC
from ..session import Session


class SessionListener(ABC):
    """Session Listener callback."""

    def on_session(self, session: Session):
        """Handle callback to handle a received session.

        Args:
            session (Session): the received Session
        """
        pass
