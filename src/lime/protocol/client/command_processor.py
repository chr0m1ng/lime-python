from abc import abstractmethod

from ..command import Command
from ..listeners import CommandListener


class CommandProcessor(CommandListener):
    """Command Processor."""

    @abstractmethod
    def process_command(self, command: Command, timeout: int) -> Command:
        """Process a Command and return the result.

        Args:
            command (Command): The Command to be processed
            timeout (int): Timeout to process the Command

        Returns:
            Command: The result Command
        """  # noqa: DAR202
        pass
