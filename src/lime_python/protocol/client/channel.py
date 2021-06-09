from asyncio import Future, get_running_loop, wait_for
from functools import partial
from typing import Callable, Dict, List
from uuid import uuid4

from ..command import Command
from ..constants import (CommandMethod, CommandStatus, CommonConstants,
                         ContentTypes, NotificationEvent, SessionState)
from ..envelope import Envelope
from ..message import Message
from ..network import Transport
from ..notification import Notification
from ..session import Session
from .channels import (CommandChannel, MessageChannel, NotificationChannel,
                       SessionChannel)
from .command_processor import CommandProcessor


class Channel(
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
        auto_reply_pings: bool = True,
        auto_notify_receipt: bool = True
    ) -> None:
        self.transport = transport
        self.auto_reply_pings = auto_reply_pings
        self.auto_notify_receipt = auto_notify_receipt
        self.state = SessionState.NEW
        self.remote_node: str = None
        self.local_node: str = None
        self.session_id: str = None
        self.command_resolves: Dict[str, Callable] = {}
        self.transport.on_envelope = self.on_envelope

    def send_message(self, message: Message) -> None:  # noqa: D102
        self.__send_only_established(message)

    def send_command(self, command: Command) -> None:  # noqa: D102
        self.__send_only_established(command)

    def send_notification(self, notification: Notification) -> None:  # noqa: D102, E501
        self.__send_only_established(notification)

    def send_session(self, session: Session) -> None:  # noqa: D102
        self.ensure_state(
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
        if command.id is None:
            command.id = str(uuid4())
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

        return future.result()

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
            if command_resolve is None:
                return
            del command_resolves[command.id]
            command.timeout = True

            raise TimeoutError(
                f'The following command processing has timed out: {command}'  # noqa: E501
            )

    def on_envelope(self, envelope: dict) -> None:  # noqa: WPS231
        """Handle received envelope on transport.

        Args:
            envelope (dict): The received raw envelope
        """
        if Envelope.is_message(envelope):
            envelope: Message = Message.from_json(envelope)
            self.__notify_message(envelope)
            self.on_message(envelope)

        elif Envelope.is_notification(envelope):
            envelope: Notification = Notification.from_json(envelope)
            self.on_notification(envelope)

        elif Envelope.is_session(envelope):
            envelope: Session = Session.from_json(envelope)
            self.on_session(envelope)

        elif Envelope.is_command(envelope):
            envelope: Command = Command.from_json(envelope)
            if hasattr(envelope, 'status') and envelope.status:
                set_result = self.command_resolves.get(envelope.id)

                if set_result:
                    set_result(envelope)
                    del self.command_resolves[envelope.id]
                    return
            if self.__should_reply_command(envelope):
                self.send_command(self.__create_ping_command_reply(envelope))
            self.on_command(envelope)

    def ensure_state(self, states: List[str], is_allowed: bool) -> None:
        """Check if class state is at specified states if it's allowed.

        Args:
            states (List[str]): List of states
            is_allowed (bool): if true check if state is at specified states\
            else if isn't

        Raises:
            ValueError: Raise if state doesn't match the is_allowed config
        """
        if (self.state in states) ^ is_allowed:
            raise ValueError(f'Cannot send in the {self.state} state')

    def __send_only_established(self, envelope: Envelope) -> None:
        self.ensure_state([SessionState.ESTABLISHED], True)
        self.__send(envelope)

    def __send(self, envelope: Envelope) -> None:
        if envelope.id is None:
            envelope.id = str(uuid4())
        self.transport.send(envelope.to_json())

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

    def __should_reply_command(self, command: Command) -> bool:
        return self.auto_reply_pings and \
            command.id and \
            command.uri == CommonConstants.PING and \
            command.method == CommandMethod.GET and \
            self.is_for_me(command)  # noqa: WPS222

    def __create_ping_command_reply(self, command: Command) -> Command:
        reply = Command(
            method=CommandMethod.GET,
            status=CommandStatus.SUCCESS,
            type_n=ContentTypes.PING,
            resource={},
        )
        reply.id = command.id
        reply.to = command.from_n
        return reply
