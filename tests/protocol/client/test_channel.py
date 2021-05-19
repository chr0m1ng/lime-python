from src.lime.protocol.client import channel
from src import Session, SessionState, Channel, Command, Message, Notification
import pytest


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


class ChannelTest(Channel):

    def on_command(self, command: Command) -> None:
        return super().on_command(command)

    def on_message(self, message: Message) -> None:
        return super().on_message(message)

    def on_notification(self, notification: Notification) -> None:
        return super().on_notification(notification)

    def on_session(self, session: Session) -> None:
        return super().on_session(session)
