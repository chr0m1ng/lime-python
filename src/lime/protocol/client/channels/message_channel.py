from abc import abstractmethod

from ...listeners import MessageListener
from ...message import Message


class MessageChannel(MessageListener):
    """Message Channel."""

    @abstractmethod
    def send_message(self, message: Message) -> None:
        """Send a message.

        Args:
            message (Message): message to be sent
        """
        pass
