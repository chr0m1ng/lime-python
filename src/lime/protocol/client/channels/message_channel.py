from ...listeners import MessageListener
from ...message import Message


class MessageChannel(MessageListener):
    """Message Channel."""

    def send_message(self, message: Message):
        """Send a message.

        Args:
            message (Message): message to be sent
        """
        pass
