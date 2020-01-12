from ..message import MessageListener
from ..command import CommandListener, CommandMethod, CommandStatus, Command
from ..notification import NotificationListener, NotificationEvent, Notification
from ..session import SessionListener, SessionState
from ..network.transport import Transport
from ..envelope import Envelope
from ...content_types import ContentTypes
import asyncio
import json


class MessageChannel(MessageListener):

    def send_message(self, message): pass


class CommandChannel(CommandListener):

    def send_command(self, command): pass


class NotificationChannel(NotificationListener):

    def send_notification(self, notification): pass


class SessionChannel(SessionListener):

    def send_session(self, session): pass


class CommandProcessor(CommandListener):

    def process_command(self, command, timeout): pass


class Channel(MessageChannel, CommandChannel, NotificationChannel, SessionChannel, CommandProcessor):

    # auto_reply_pings property
    @property
    def auto_reply_pings(self):
        return self.__auto_reply_pings

    @auto_reply_pings.setter
    def auto_reply_pings(self, value):
        if isinstance(value, bool):
            self.__auto_reply_pings = value
        else:
            raise ValueError('auto_reply_pings must be a bool')

    # auto_notify_receipt property
    @property
    def auto_notify_receipt(self):
        return self.__auto_notify_receipt

    @auto_notify_receipt.setter
    def auto_notify_receipt(self, value):
        if isinstance(value, bool):
            self.__auto_notify_receipt = value
        else:
            raise ValueError('auto_notify_receipt must be a bool')

    # __command_futures property
    @property
    def __command_futures(self):
        return self.__command_futures

    @__command_futures.setter
    def __command_futures(self, value):
        if isinstance(value, dict):
            self.__command_futures = value
        else:
            raise ValueError('__command_futures must be a dict')

    # transport property
    @property
    def transport(self):
        return self.__transport

    @transport.setter
    def transport(self, value):
        if isinstance(value, Transport):
            self.__transport = value
        else:
            raise ValueError('transport must be a Transport')

    # remote_node property
    @property
    def remote_node(self):
        return self.__remote_node

    @remote_node.setter
    def remote_node(self, value):
        if isinstance(value, str):
            self.__remote_node = value
        else:
            raise ValueError('remote_node must be a str')

    # local_node property
    @property
    def local_node(self):
        return self.__local_node

    @local_node.setter
    def local_node(self, value):
        if isinstance(value, str):
            self.__local_node = value
        else:
            raise ValueError('local_node must be a str')

    # session_id property
    @property
    def session_id(self):
        return self.__session_id

    @session_id.setter
    def session_id(self, value):
        if isinstance(value, str):
            self.__session_id = value
        else:
            raise ValueError('session_id must be a str')

    # state property
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        if isinstance(value, SessionState):
            self.__state = value
        else:
            raise ValueError('state must be a SessionState')

    # Timout in seconds
    command_timeout = 6

    def __init__(self, transport, auto_reply_pings, auto_notify_receipt):
        self.auto_reply_pings = auto_reply_pings
        self.auto_notify_receipt = auto_notify_receipt
        self.transport = transport
        self.__command_futures = dict()
        self.state = SessionState.NEW

        def transport_on_envelope(envelope):
            # Message
            if Envelope.is_message(envelope):
                message = envelope
                self.notify_message(message)
                self.on_message(message)
            # Notification
            elif Envelope.is_notification(envelope):
                notification = envelope
                self.on_notification(notification)
            # Command
            elif Envelope.is_command(envelope):
                command = envelope

                if command.status is not None:
                    if command.id in self.__command_futures:
                        self.__command_futures[command.id](command)
                        del self.__command_futures[command.id]
                        return

                if self.auto_reply_pings and command.id is not None and \
                        command.uri == '/ping' and command.method == CommandMethod.GET and \
                        self.is_for_me(command):
                    ping_command_response = Command()
                    ping_command_response.id = command.id
                    ping_command_response.to_n = command.from_n
                    ping_command_response.method = CommandMethod.GET
                    ping_command_response.status = CommandStatus.SUCCESS
                    ping_command_response.resource_type = ContentTypes.PING
                    ping_command_response.resource = dict()

                    self.send_command(ping_command_response)

                self.on_command(command)
            # Session
            elif Envelope.is_session(envelope):
                session = envelope
                self.on_session(session)

        self.transport.on_envelope = transport_on_envelope

    def send(self, envelope):
        self.transport.send(envelope)

    def send_message(self, message):
        if self.state != SessionState.ESTABLISHED:
            raise Exception(f'Cannot send in the {self.state.value} state')
        self.send(message)

    def on_message(self, message): raise NotImplementedError

    def send_command(self, command):
        if self.state != SessionState.ESTABLISHED:
            raise Exception(f'Cannot send in the {self.state.value} state')
        self.send(command)

    def process_command(self, command, timeout=Channel.command_timeout):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        response_future = loop.create_future()

        self.__command_futures[command.id] = response_future.set_result

        async def loop_command_timeout():
            await asyncio.sleep(timeout)

            if command.id not in self.__command_futures:
                return

            del self.__command_futures[command.id]

            # Implement a custom JSONEncoder to use in json.dumps
            cmd = command.__dict__
            response_future.set_exception(
                TimeoutError(
                    f'The follow command processing has timed out: {cmd}'
                )
            )

        asyncio.ensure_future(loop_command_timeout)

        self.send_command(command)

        return response_future

    def on_command(self, command): raise NotImplementedError

    def send_notification(self, notification):
        if self.state != SessionState.ESTABLISHED:
            raise Exception(f'Cannot send in the {self.state.value} state')

        self.send(notification)

    def on_notification(self, notification): raise NotImplementedError

    def send_session(self, session):
        if self.state == SessionState.FINISHED or self.state == SessionState.FAILED:
            raise Exception(f'Cannot send in the {self.state.value} state')
        self.send(session)

    def on_session(self, session): raise NotImplementedError

    def notify_message(self, message):
        if self.auto_notify_receipt and message.id is not None and \
                message.from_n is not None and self.is_for_me(message):
            notification = Notification()
            notification.id = message.id
            notification.from_n = message.from_n
            notification.event = NotificationEvent.RECEIVED

            self.send_notification(notification)

    def is_for_me(self, envelope):
        return envelope.to_n is None or \
            envelope.to_n == self.local_node or \
            self.local_node[:len(envelope.to_n)] == envelope.to_n
