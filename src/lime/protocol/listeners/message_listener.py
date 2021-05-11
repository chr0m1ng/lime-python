from abc import ABC
from src.lime.protocol import Message


class MessageListener(ABC):
    """Message listener callback."""

    def on_message(self, command: Message):
        """Handle callback to received event.

        Args:
            command (Message): Command being received
        """
        pass
