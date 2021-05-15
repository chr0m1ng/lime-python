from abc import abstractmethod
from ...listeners import MessageListener
from ...message import Message


class MessageChannel(MessageListener):
    """Message channel representation."""

    @abstractmethod
    def send_message(self, message: Message):
        """Send message command.

        Args:
            message (Message): receive message
        """
        pass
