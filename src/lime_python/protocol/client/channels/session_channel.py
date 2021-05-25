from abc import abstractmethod

from ...listeners import SessionListener
from ...session import Session


class SessionChannel(SessionListener):
    """Session Channel."""

    @abstractmethod
    def send_session(self, session: Session) -> None:
        """Send a Session.

        Args:
            session (Session): Session to be sent
        """
        pass
