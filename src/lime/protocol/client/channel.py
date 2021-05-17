from abc import abstractmethod
from ..constants import SessionState
from .command_processor import CommandProcessor
from .channels import MessageChannel, NotificationChannel, SessionChannel, CommandChannel  # noqa: E501
from ..envelope import Envelope
from ..message import Message
from ..command import Command
from ..notification import Notification
from ..network import Transport


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
        """Send message.
        Args:
            message (Message): message to be sended
        """
        self.send_envelope(message)

    def on_message(self, message: Message):
        pass

    def send_notification(self, notification: Notification):
        """Send notification.
         Args:
             notification (Notification): notification to be sended
         """
        self.send_envelope(notification)

    def on_notification(self, notification: Notification):
        pass

    def __send(self, envelope: Envelope):
        self.transport.send(envelope)
