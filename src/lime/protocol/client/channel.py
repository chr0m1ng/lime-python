from asyncio import Future, get_running_loop, wait_for
from functools import partial
from typing import Callable, Dict, List

from ..command import Command
from ..constants import NotificationEvent, SessionState
from ..envelope import Envelope
from ..message import Message
from ..network import Transport
from ..notification import Notification
from ..session import Session
from .channels import CommandChannel, MessageChannel, NotificationChannel, SessionChannel  # noqa: 319
from .command_processor import CommandProcessor  # noqa: I005


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
        self.command_resolves: Dict[str, Callable] = {}

    def send_message(self, message: Message) -> None:  # noqa: D102
        self.__send_only_established(message)

    def send_command(self, command: Command) -> None:  # noqa: D102
        self.__send_only_established(command)

    def send_notification(self, notification: Notification) -> None:  # noqa: D102, E501
        self.__send_only_established(notification)

    def send_session(self, session: Session) -> None:  # noqa: D102
        self.__ensure_state(
            [SessionState.FINISHED, SessionState.FAILED],
            False
        )
        self.__send(session)

    async def process_command_async(  # noqa: D102
        self,
        command: Command,
        timeout: float
    ) -> Command:
        loop = get_running_loop()
        future = loop.create_future()
        self.command_resolves[command.id] = future.set_result

        self.send_command(command)

        future.add_done_callback(
            partial(
                Channel.raise_command_timeout,
                command=command,
                command_resolves=self.command_resolves
            )
        )
        await wait_for(future, timeout)

        return future

    @staticmethod
    def raise_command_timeout(
        fut: Future,
        command: Command,
        command_resolves: Dict[str, Callable]
    ) -> None:
        """Raise a command timeout.

        Args:
            fut (Future): the originator future
            command (Command): the timed out sent command
            command_resolves (Dict[str, Callable]): the dictionary of futures resolves

        Raises:
            TimeoutError: Command could not be processed in the given timeout
        """  # noqa: E501
        if fut.cancelled():
            command_resolve = command_resolves.get(command.id)
            if command_resolve is not None:
                del command_resolves[command.id]

            raise TimeoutError(
                f'The following command processing has timed out: {command}'
            )

    def __ensure_state(self, states: List[str], is_allowed: bool) -> None:
        if self.state in states ^ is_allowed:
            raise ValueError(f'Cannot send in the {self.state} state')

    def __send_only_established(self, envelope: Envelope) -> None:
        self.__ensure_state([SessionState.ESTABLISHED], True)
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
