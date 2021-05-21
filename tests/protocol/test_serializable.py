from src import Serializable


class TestSerializable:
    def test_normalize_key(self):
        # Arrange
        node_key = 'from_n'
        target = self.get_target()

        expected_result = 'from'

        # Act
        result = target.normalize_key(node_key)

        # Assert
        assert result == expected_result

    def test_serialize_value_native(self):
        # Arrange
        value = 123
        target = self.get_target()

        # Act
        result = target.serialize_value(value)

        # Assert
        assert result == value

    def test_serialize_value_serializable(self):
        # Arrange
        value = DummySerializable()
        target = self.get_target()

        # Act
        result = target.serialize_value(value)

        # Assert
        assert result == value.to_json()

    def test_to_json(self):
        # Arrange

        class Mock(Serializable):
            batata = 123

            def __init__(self):
                self.mock = 'value'
                self.some_n = 123
                self.__private = 'not-showing'
                self.not_showing = None

        mock = Mock()

        expected_result = {
            'mock': 'value',
            'some': 123
        }

        # Act
        result = mock.to_json()

        # Assert
        assert result == expected_result

    def get_target(self):
        return Serializable()


class DummySerializable(Serializable):

    def __init__(self) -> None:
        self.dummy = 'dummy'
