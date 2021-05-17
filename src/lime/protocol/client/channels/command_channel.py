from abc import abstractmethod

from ...command import Command
from ...listeners import CommandListener


class CommandChannel(CommandListener):
    """Command Channel."""

    @abstractmethod
    def send_command(self, command: Command) -> None:
        """Send a Command.

        Args:
            command (Command): Command to be sent
        """
        pass
