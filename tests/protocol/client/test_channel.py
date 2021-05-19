from src.lime.protocol.constants.command_status import CommandStatus
from src import (SessionCompression, SessionEncryption, Envelope,
                 Session, SessionState, Channel, Command, Message,
                 Notification, CommandMethod, Channel, Transport,
                 UriTemplates, ContentTypes)
from typing import List, Callable
import pytest
from asyncio import TimeoutError, wait, sleep, create_task
from functools import partial


class TestChannel:

    def test_ensure_allowed_states(self):
        # Arrange
        channel = ChannelTest(None, False, False)
        session = Session(SessionState.AUTHENTICATING)
        channel.state = SessionState.FAILED

        # Assert
        with pytest.raises(ValueError):
            channel.send_command(session)

    def test_ensure_not_allowed_states(self):
        # Arrange
        channel = ChannelTest(None, False, False)
        session = Session(SessionState.AUTHENTICATING)
        channel.state = SessionState.FAILED

        # Assert
        with pytest.raises(ValueError):
            channel.send_command(session)

    @pytest.mark.asyncio
    async def test_process_command_timeout_async(self):
        # Arrange
        transport = TransportTest(
            SessionCompression.NONE,
            SessionEncryption.TLS
        )
        channel = ChannelTest(transport, None, False)
        channel.state = SessionState.ESTABLISHED
        command = Command(CommandMethod.GET, '/context')

        # Assert
        with pytest.raises(TimeoutError):
            await channel.process_command_async(command, 1.0)

    @pytest.mark.asyncio
    async def test_process_command_async(self):
        # Arrange
        transport = TransportTest(
            SessionCompression.NONE,
            SessionEncryption.TLS
        )

        channel = ChannelTest(transport, None, False)
        channel.state = SessionState.ESTABLISHED

        command = Command(CommandMethod.GET, UriTemplates.PING)
        command.id = '1234'
        command_response = {
            'id': '1234',
            'method': CommandMethod.GET,
            'type': ContentTypes.PING,
            'resource': {},
            'status': CommandStatus.SUCCESS
        }

        process_command = create_task(
            channel.process_command_async(command, 10.0),
            name='process_command'
        )

        on_envelope = create_task(self.act_with_delay_async(
            partial(channel.on_envelope, envelope=command_response),
            2
        ))

        # Act
        done, pending = await wait({process_command, on_envelope})
        result: Command = {
            f.result()
            for f in done
            if f.get_name() == 'process_command'
        }.pop()

        # Assert
        assert len(pending) == 0
        assert result.to_json() == command_response

    async def act_with_delay_async(self, act: Callable, delay: int):
        await sleep(delay)
        act()


class ChannelTest(Channel):

    def on_command(self, command: Command) -> None:
        return super().on_command(command)

    def on_message(self, message: Message) -> None:
        return super().on_message(message)

    def on_notification(self, notification: Notification) -> None:
        return super().on_notification(notification)

    def on_session(self, session: Session) -> None:
        return super().on_session(session)


class TransportTest(Transport):

    def send(self, envelope: Envelope):
        return super().send(envelope)

    def get_supported_compression(self) -> List[str]:
        return super().get_supported_compression()

    def get_supported_encryption(self) -> List[str]:
        return super().get_supported_encryption()

    def on_envelope(self, envelope: Envelope) -> None:
        return super().on_envelope(envelope)

    def open(self, uri: str):
        return super().open(uri)

    def set_compression(self, compression: str):
        return super().set_compression(compression)

    def set_encryption(self, encryption: str):
        return super().set_encryption(encryption)

    def close(self):
        return super().close()
