from src import Command, Envelope, Message, Notification, Session


class TestEnvelope:

    def test_is_message_should_be_true(self):
        # Arrange
        envelope = Message('application/json', {'some': 'content'})

        # Act
        result = Envelope.is_message(envelope)

        # Assert
        assert result is True

    def test_is_message_should_be_false(self):
        # Arrange
        envelope = Notification('consumed')

        # Act
        result = Envelope.is_message(envelope)

        # Assert
        assert result is False

    def test_is_notification_should_be_true(self):
        # Arrange
        envelope = Notification('consumed')

        # Act
        result = Envelope.is_notification(envelope)

        # Assert
        assert result is True

    def test_is_notification_should_be_false(self):
        # Arrange
        envelope = Session('new')

        # Act
        result = Envelope.is_notification(envelope)

        # Assert
        assert result is False

    def test_is_command_should_be_true(self):
        # Arrange
        envelope = Command('get')

        # Act
        result = Envelope.is_command(envelope)

        # Assert
        assert result is True

    def test_is_command_should_be_false(self):
        # Arrange
        envelope = Session('new')

        # Act
        result = Envelope.is_command(envelope)

        # Assert
        assert result is False

    def test_is_session_should_be_true(self):
        # Arrange
        envelope = Session('new')

        # Act
        result = Envelope.is_session(envelope)

        # Assert
        assert result is True

    def test_is_session_should_be_false(self):
        # Arrange
        envelope = Command('get')

        # Act
        result = Envelope.is_session(envelope)

        # Assert
        assert result is False
