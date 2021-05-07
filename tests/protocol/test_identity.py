from src import Identity


class TestSerializabe:
    def test_parse_str(self):
        # Arrange
        identity = 'test@take.net'

        expected_result = Identity('test', 'take.net')

        # Act
        result = Identity.parse_str(identity)

        # Assert
        assert result == expected_result
