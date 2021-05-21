from abc import ABC, abstractmethod

from ..session import Session


class SessionListener(ABC):
    """Session Listener callback."""

    @abstractmethod
    def on_session(self, session: Session) -> None:
        """Handle callback to handle a received session.

        Args:
            session (Session): the received Session
        """
        pass
