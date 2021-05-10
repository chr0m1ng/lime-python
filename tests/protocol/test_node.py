from src import Identity, Node

TEST_IDENTITY_DOMAIN = 'take.net'
TEST_IDENTITY_NAME = 'test'
TEST_INSTANCE = 'iris4'


class TestNode:

    def test_parse_str(self):

        # Arrange
        node = f'{TEST_IDENTITY_NAME}@{TEST_IDENTITY_DOMAIN}/{TEST_INSTANCE}'
        identity = Identity(TEST_IDENTITY_NAME, TEST_IDENTITY_DOMAIN)
        expected_result = Node(identity, TEST_INSTANCE)

        # Act
        result = Node.parse_str(node)

        # Assert
        assert expected_result == result

    def test_parse_from_identity(self):

        # Arrange
        identity = Identity(TEST_IDENTITY_NAME, TEST_IDENTITY_DOMAIN)

        expected_result = Node(identity, str())

        # Act
        result = Node.parse(identity)

        # Assert
        assert expected_result == result

    def test_parse_from_node(self):

        # Arrange
        identity = Identity(TEST_IDENTITY_NAME, TEST_IDENTITY_DOMAIN)
        node = Node(identity, TEST_INSTANCE)

        # Act
        result = Node.parse(node)

        # Assert
        assert node == result
