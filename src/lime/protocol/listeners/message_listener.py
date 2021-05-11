from abc import ABC
from ..message import Message


class MessageListener(ABC):
    """Message listener callback."""

    def on_message(self, message: Message):
        """Handle callback to handle a received Message.

        Args:
            message (Message): the received Message
        """
        pass
