from typing import List
from ..command import Command
from ..constants import SessionState, NotificationEvent
from ..envelope import Envelope
from ..message import Message
from ..network import Transport
from ..notification import Notification
from ..session import Session
from .channels import (CommandChannel, MessageChannel,
                       NotificationChannel, SessionChannel)  # noqa: 319
from .command_processor import CommandProcessor


class Channel(  # noqa: WPS215, WPS230
    MessageChannel,
    NotificationChannel,
    SessionChannel,
    CommandChannel,
    CommandProcessor
):
    """Channel to communicate with Envelopes."""

    def __init__(
        self,
        transport: Transport,
        auto_reply_pings: bool,
        auto_notify_receipt: bool
    ):
        self.transport = transport
        self.auto_reply_pings = auto_reply_pings
        self.auto_notify_receipt = auto_notify_receipt
        self.state = SessionState.NEW
        self.remote_node: str = None
        self.local_node: str = None
        self.session_id: str = None

    def send_message(self, message: Message) -> None:  # noqa: D102
        self.__send_only_established(message)

    def send_command(self, command: Command) -> None:  # noqa: D102
        self.__send_only_established(command)

    def send_notification(self, notification: Notification) -> None:  # noqa: D102, E501
        self.__send_only_established(notification)

    def send_session(self, session: Session) -> None:  # noqa: D102
        self.__ensure_not_in_states(
            [SessionState.FINISHED, SessionState.FAILED]
        )
        self.__send(session)

    async def process_command_async(  # noqa: D102
        self,
        command: Command,
        timeout: int
    ) -> Command:
        pass

    def __ensure_not_in_states(self, states: List[str]) -> None:
        if self.state in states:
            raise ValueError(f'Cannot send in the {self.state} state')

    def __send_only_established(self, envelope: Envelope) -> None:
        self.__ensure_not_in_states([SessionState.ESTABLISHED])
        self.__send(envelope)

    def __send(self, envelope: Envelope) -> None:
        self.transport.send(envelope)

    def __notify_message(self, message: Message) -> None:
        if self.__should_notify_message(message):
            notification = Notification(NotificationEvent.RECEIVED)
            notification.id = message.id
            notification.to = message.to
            self.send_notification(notification)

    def __should_notify_message(self, message: Message) -> bool:
        return self.auto_notify_receipt and\
            message.id is not None and\
            message.from_n is not None and\
            self.__is_for_me(message)

    def __is_for_me(self, envelope: Envelope) -> bool:
        return envelope.to is None or \
            envelope.to == self.local_node or \
            self.local_node.startswith(envelope.to)
