from typing import Dict

from .serializable import Serializable


class Envelope(Serializable):
    """Envelope representation."""

    def __init__(
        self,
        id: str = None,
        from_n: str = None,
        to: str = None,
        pp: str = None,
        metadata: Dict[str, str] = None
    ):
        self.id = id
        self.from_n = from_n
        self.to = to
        self.pp = pp
        self.metadata = metadata

    @staticmethod
    def is_message(envelope) -> bool:
        """Check if a envelope is a Message.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Message
        """
        return hasattr(envelope, 'content')

    @staticmethod
    def is_notification(envelope) -> bool:
        """Check if a envelope is a Notification.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Notification
        """
        return hasattr(envelope, 'event')

    @staticmethod
    def is_command(envelope) -> bool:
        """Check if a envelope is a Command.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Command
        """
        return hasattr(envelope, 'method')

    @staticmethod
    def is_session(envelope) -> bool:
        """Check if a envelope is a Session.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Session
        """
        return hasattr(envelope, 'state')
