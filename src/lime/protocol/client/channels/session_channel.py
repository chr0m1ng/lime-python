from abc import abstractmethod
from ...listeners import SessionListener
from ...session import Session


class SessionChannel(SessionListener):
    """Session channel representaiton."""

    @abstractmethod
    def send_session(self, session: Session):
        """Send session.

        Args:
            session (Session): Session received
        """
        pass
