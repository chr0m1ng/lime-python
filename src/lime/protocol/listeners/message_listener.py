from abc import ABC, abstractmethod

from ..message import Message


class MessageListener(ABC):
    """Message listener callback."""

    @abstractmethod
    def on_message(self, message: Message) -> None:
        """Handle callback to handle a received Message.

        Args:
            message (Message): the received Message
        """
        pass
