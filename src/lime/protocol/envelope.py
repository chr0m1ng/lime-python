from abc import ABC
from typing import Dict

from .serializable import Serializable


class Envelope(ABC, Serializable):
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
        return isinstance(envelope, Serializable) \
            and 'content' in envelope.to_json()

    @staticmethod
    def is_notification(envelope) -> bool:
        """Check if a envelope is a Notification.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Notification
        """
        return isinstance(envelope, Serializable) \
            and 'event' in envelope.to_json()

    @staticmethod
    def is_command(envelope) -> bool:
        """Check if a envelope is a Command.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Command
        """
        return isinstance(envelope, Serializable) \
            and 'method' in envelope.to_json()

    @staticmethod
    def is_session(envelope) -> bool:
        """Check if a envelope is a Session.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Session
        """
        return isinstance(envelope, Serializable) \
            and 'state' in envelope.to_json()
