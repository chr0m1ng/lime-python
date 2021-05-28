from pytest import fixture
from src import Serializable


class TestSerializable:

    @fixture
    def target(self) -> Serializable:
        return Serializable()

    def test_normalize_key(self, target: Serializable) -> None:
        # Arrange
        node_key = 'from_n'
        expected_result = 'from'

        # Act
        result = target.normalize_key(node_key)

        # Assert
        assert result == expected_result

    def test_serialize_value_native(self, target: Serializable) -> None:
        # Arrange
        value = 123

        # Act
        result = target.serialize_value(value)

        # Assert
        assert result == value

    def test_serialize_value_serializable(self, target: Serializable) -> None:
        # Arrange
        value = DummySerializable()

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
                self.should_be_in_camel = 'yes'

        mock = Mock()

        expected_result = {
            'mock': 'value',
            'some': 123,
            'shouldBeInCamel': 'yes'
        }

        # Act
        result = mock.to_json()

        # Assert
        assert result == expected_result

    def test_from_json(self):
        # Arrange
        class Mock(Serializable):
            batata = 123

            def __init__(self):
                self.mock = 'value'
                self.some_n = 123
                self.__private = 'not-showing'
                self.not_showing = None
                self.should_be_in_camel = 'yes'

        expected_result = Mock()

        raw_json = {
            'mock': 'value',
            'some': 123,
            'shouldBeInCamel': 'yes'
        }

        # Act
        result = Mock.from_json(raw_json)

        # Assert
        assert result == expected_result


class DummySerializable(Serializable):

    def __init__(self) -> None:
        self.dummy = 'dummy'
