class Reason:
    """A reason for events occurred during the client-server interactions."""

    def __init__(self, code: int, description: str):
        self.code = code
        self.description = description

    def __str__(self):
        """Override str representation.

        Returns:
            str: description with code
        """
        return f'{self.description} (Code {self.code.value})'
