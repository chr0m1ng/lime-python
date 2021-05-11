from src import Identity, Node

TEST_IDENTITY_DOMAIN = 'take.net'
TEST_IDENTITY_NAME = 'test'


class TestSerializabe:

    def test_parse_from_identity(self):
        # Arrange
        identity = Identity(TEST_IDENTITY_NAME, TEST_IDENTITY_DOMAIN)

        # Act
        result = Identity.parse(identity)

        # Assert
        assert result == identity

    def test_parse_from_node(self):
        # Arrange
        expected_result = Identity(TEST_IDENTITY_NAME, TEST_IDENTITY_DOMAIN)

        identity = Node(expected_result, 'iris2')

        # Act
        result = Identity.parse(identity)

        # Assert
        assert result == expected_result

    def test_parse_from_str(self):
        # Arrange
        identity = f'{TEST_IDENTITY_NAME}@{TEST_IDENTITY_DOMAIN}'

        expected_result = Identity(TEST_IDENTITY_NAME, TEST_IDENTITY_DOMAIN)

        # Act
        result = Identity.parse(identity)

        # Assert

        assert result == expected_result
