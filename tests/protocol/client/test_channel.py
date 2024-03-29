from asyncio import TimeoutError, ensure_future, sleep
from typing import Callable

import pytest
from pytest_mock import MockerFixture

from src import (Channel, Command, CommandMethod, CommandStatus,
                 CommonConstants, ContentTypes, Message, Notification,
                 NotificationEvent, Session, SessionCompression,
                 SessionEncryption, SessionState)

from .transport_dummy import TransportDummy


class TestChannel:

    def test_ensure_allowed_states(self) -> None:
        # Arrange
        channel = self.__get_target(SessionState.FAILED)
        session = Session(SessionState.AUTHENTICATING)

        # Assert
        with pytest.raises(ValueError):
            channel.send_command(session)

    def test_ensure_not_allowed_states(self) -> None:
        # Arrange
        channel = self.__get_target(SessionState.FAILED)
        session = Session(SessionState.AUTHENTICATING)

        # Assert
        with pytest.raises(ValueError):
            channel.send_command(session)

    @pytest.mark.asyncio
    async def test_process_command_timeout_async(self) -> None:
        # Arrange
        channel = self.__get_target()
        command = Command(CommandMethod.GET, CommonConstants.PING)

        # Assert
        with pytest.raises(TimeoutError):
            await channel.process_command_async(command, 1.0)

    @pytest.mark.asyncio
    async def test_process_command_async(self) -> None:
        # Arrange
        channel = self.__get_target()

        command = Command(CommandMethod.GET, CommonConstants.PING)
        command.id = '1234'
        command_response = {
            'id': '1234',
            'method': CommandMethod.GET,
            'type': ContentTypes.PING,
            'resource': {},
            'status': CommandStatus.SUCCESS
        }

        ensure_future(
            self.set_timeout(
                1,
                lambda: channel.on_envelope(command_response)
            )
        )

        # Act
        result: Command = await channel.process_command_async(command, 3)

        # Assert
        assert result == Command.from_json(command_response)

    async def set_timeout(self, timeout: float, action: Callable) -> None:
        await sleep(timeout)
        action()

    def test_on_envelope_message(self, mocker: MockerFixture) -> None:
        # Arrange
        channel = self.__get_target()
        message = Message(ContentTypes.PING, {})
        spy = mocker.spy(channel, 'on_message')

        # Act
        channel.on_envelope(message.to_json())

        # Assert
        spy.assert_called_once_with(message)

    def test_on_envelope_notification(self, mocker: MockerFixture) -> None:
        # Arrange
        channel = self.__get_target()
        notification = Notification(NotificationEvent.CONSUMED)
        spy = mocker.spy(channel, 'on_notification')

        # Act
        channel.on_envelope(notification.to_json())

        # Assert
        spy.assert_called_once_with(notification)

    def test_on_envelope_session(self, mocker: MockerFixture) -> None:
        # Arrange
        channel = self.__get_target()
        session = Session(SessionState.FINISHED)
        spy = mocker.spy(channel, 'on_session')

        # Act
        channel.on_envelope(session.to_json())

        # Assert
        spy.assert_called_once_with(session)

    def test_on_envelope_command(self, mocker: MockerFixture) -> None:
        # Arrange
        channel = self.__get_target()
        command = Command(CommandMethod.GET)
        spy = mocker.spy(channel, 'on_command')

        # Act
        channel.on_envelope(command.to_json())

        # Assert
        spy.assert_called_once_with(command)

    def __get_target(self, state: str = SessionState.ESTABLISHED) -> Channel:
        transport = TransportDummy(
            SessionCompression.NONE,
            SessionEncryption.TLS
        )

        channel = ChannelTest(transport, None, False)
        channel.state = state
        return channel


class ChannelTest(Channel):

    def on_command(self, command: Command) -> None:
        pass

    def on_message(self, message: Message) -> None:
        pass

    def on_notification(self, notification: Notification) -> None:
        pass

    def on_session(self, session: Session) -> None:
        pass
