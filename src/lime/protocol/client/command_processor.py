from abc import abstractmethod
from ..command import Command
from ..listeners import CommandListener


class CommandProcessor(CommandListener):
    """Command processor representation."""

    @abstractmethod
    def process_command(self, command: Command, timeout: int):
        """Process command.

        Args:
            command (Command): command received
            timeout (int): specified timeout
        """
        pass
