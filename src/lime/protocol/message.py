from abc import ABC
from .envelope import Envelope


class Message(Envelope):
    """Message representation."""

    def __init__(self, type_n: str, content):
        self.type_n = type_n
        self.content = content


class MessageListener(ABC):
    """Message listener callback."""

    def on_message(self, command: Message):
        """Handle callback to received event.

        Args:
            command (Message): Command being received
        """
        pass
