from ...listeners import SessionListener
from ...session import Session


class SessionChannel(SessionListener):
    """Session Channel."""

    def send_session(self, session: Session):
        """Send a Session.

        Args:
            session (Session): Session to be sent
        """
        pass
