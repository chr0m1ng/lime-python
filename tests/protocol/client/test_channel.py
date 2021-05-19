from src import (SessionCompression, SessionEncryption, Envelope,
                 Session, SessionState, Channel, Command, Message,
                 Notification, CommandMethod, Channel, Transport)
from typing import List
import pytest
from asyncio import TimeoutError


class TestChannel:

    def test_ensure_allowed_states(self):
        # Arrange
        channel = ChannelTest(None, False, False)
        session = Session(SessionState.AUTHENTICATING)
        channel.state = 'failed'

        # Assert
        with pytest.raises(ValueError):
            channel.send_command(session)

    def test_ensure_not_allowed_states(self):
        # Arrange
        channel = ChannelTest(None, False, False)
        session = Session(SessionState.AUTHENTICATING)
        channel.state = 'failed'

        # Assert
        with pytest.raises(ValueError):
            channel.send_command(session)

    @pytest.mark.asyncio
    async def test_process_comand_timeout_async(self):
        # Arrange
        transport = TransportTest(
            SessionCompression.NONE, SessionEncryption.TLS)
        channel = ChannelTest(transport, None, False)
        channel.state = SessionState.ESTABLISHED
        command = Command(
            CommandMethod.GET,
            '/context')

        # Assert
        with pytest.raises(TimeoutError):
            (await channel.process_command_async(command, 1.0))


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
