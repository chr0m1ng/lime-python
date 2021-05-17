from ..command import Command
from ..constants import SessionState
from ..envelope import Envelope
from ..message import Message
from ..network import Transport
from ..notification import Notification
from .channels import (CommandChannel, MessageChannel,
                       NotificationChannel, SessionChannel)  # noqa: 319
from .command_processor import CommandProcessor


class Channel(  # noqa: WPS215
    MessageChannel,
    NotificationChannel,
    SessionChannel,
    CommandChannel,
    CommandProcessor
):

    def __init__(
        self,
        transport: Transport,
        auto_reply_pings: bool,
        auto_notification_receipt: bool
    ):
        self.state = SessionState.NEW
        self.transport = transport
        self.auto_reply_pings = auto_reply_pings
        self.auto_notification_receipt = auto_notification_receipt

    def on_envelope(self, envelope: Envelope):
        # message
        if Envelope.is_message(envelope):
            message = envelope

    def send_envelope(self, envelope: Envelope):
        """Send generic envelope.
        Args:
            envelope (Message | Notification): Envelope Received
        Raises:
            Exception: Unable to send envelope exception
        """
        if self.state != SessionState.ESTABLISHED:
            raise Exception(f'Cannot send in the {self.state} state')
        self.__send(envelope)

    def send_message(self, message: Message):
        """Send a message.

        Args:
            message (Message): message to be sent
        """
        self.send_envelope(message)

    def on_message(self, message: Message):
        """Handle callback to handle a received Message.

        Args:
            message (Message): the received Message
        """
        pass

    def send_notification(self, notification: Notification):
        """Send a Notification.

        Args:
            notification (Notification): Notification to be sent
        """
        self.send_envelope(notification)

    def on_notification(self, notification: Notification):
        """Handle callback to handle a received notification.

        Args:
            notification (Notification): the received Notification
        """
        pass

    def __send(self, envelope: Envelope):
        self.transport.send(envelope)
