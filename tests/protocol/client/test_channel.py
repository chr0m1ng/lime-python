from asyncio import TimeoutError, create_task, sleep, wait
from functools import partial
from typing import Callable, List

import pytest
from pytest_mock import MockerFixture

from src import (Channel, Command, CommandMethod, CommandStatus, ContentTypes,
                 Envelope, Message, Notification, NotificationEvent, Session,
                 SessionCompression, SessionEncryption, SessionState,
                 Transport, UriTemplates)


class TestChannel:

    def test_ensure_allowed_states(self):
        # Arrange
        channel = self.__get_target(SessionState.FAILED)
        session = Session(SessionState.AUTHENTICATING)

        # Assert
        with pytest.raises(ValueError):
            channel.send_command(session)

    def test_ensure_not_allowed_states(self):
        # Arrange
        channel = self.__get_target(SessionState.FAILED)
        session = Session(SessionState.AUTHENTICATING)

        # Assert
        with pytest.raises(ValueError):
            channel.send_command(session)

    @pytest.mark.asyncio
    async def test_process_command_timeout_async(self):
        # Arrange
        channel = self.__get_target()
        command = Command(CommandMethod.GET, UriTemplates.PING)

        # Assert
        with pytest.raises(TimeoutError):
            await channel.process_command_async(command, 1.0)

    @pytest.mark.asyncio
    async def test_process_command_async(self):
        # Arrange
        channel = self.__get_target()

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
            channel.process_command_async(command, 10.0)  # noqa: WPS432
        )

        on_envelope = create_task(self.act_with_delay_async(
            partial(channel.on_envelope, envelope=command_response),
            2
        ))

        # Act
        done, pending = await wait({process_command, on_envelope})
        result: Command = {
            task.result()
            for task in done
            if task.result()
        }.pop()

        # Assert
        assert bool(pending) is False
        assert result.to_json() == command_response

    async def act_with_delay_async(self, act: Callable, delay: int):
        await sleep(delay)
        act()

    def test_on_envelope_message(self, mocker: MockerFixture):
        # Arrange
        channel = self.__get_target()
        message = Message(ContentTypes.PING, {})
        spy = mocker.spy(channel, 'on_message')

        # Act
        channel.on_envelope(message.to_json())

        # Assert
        spy.assert_called_once_with(message)

    def test_on_envelope_notification(self, mocker: MockerFixture):
        # Arrange
        channel = self.__get_target()
        notification = Notification(NotificationEvent.CONSUMED)
        spy = mocker.spy(channel, 'on_notification')

        # Act
        channel.on_envelope(notification.to_json())

        # Assert
        spy.assert_called_once_with(notification)

    def test_on_envelope_session(self, mocker: MockerFixture):
        # Arrange
        channel = self.__get_target()
        session = Session(SessionState.FINISHED)
        spy = mocker.spy(channel, 'on_session')

        # Act
        channel.on_envelope(session.to_json())

        # Assert
        spy.assert_called_once_with(session)

    def test_on_envelope_command(self, mocker: MockerFixture):
        # Arrange
        channel = self.__get_target()
        command = Command(CommandMethod.GET)
        spy = mocker.spy(channel, 'on_command')

        # Act
        channel.on_envelope(command.to_json())

        # Assert
        spy.assert_called_once_with(command)

    def __get_target(self, state: str = SessionState.ESTABLISHED):
        transport = TransportTest(
            SessionCompression.NONE,
            SessionEncryption.TLS
        )

        channel = ChannelTest(transport, None, False)
        channel.state = state
        return channel


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
