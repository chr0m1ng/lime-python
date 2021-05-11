from abc import ABC
from .serializable import Serializable


class Envelope(ABC, Serializable):
    """Envelope representation."""

    def __init__(self, id: str, from_n: str, to: str, pp: str, metadata: dict):
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
        return 'content' in envelope

    @staticmethod
    def is_notification(envelope) -> bool:
        """Check if a envelope is a Notification.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Notification
        """
        return 'event' in envelope

    @staticmethod
    def is_command(envelope) -> bool:
        """Check if a envelope is a Command.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Command
        """
        return 'method' in envelope

    @staticmethod
    def is_session(envelope) -> bool:
        """Check if a envelope is a Session.

        Args:
            envelope (Envelope): the Envelope to be checked

        Returns:
            bool: True if the given Envelope is a Session
        """
        return 'state' in envelope
