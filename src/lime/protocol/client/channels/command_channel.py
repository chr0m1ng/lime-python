from abc import abstractmethod
from ...command import Command
from ...listeners import CommandListener


class CommandChannel(CommandListener):
    """Command channel representation."""

    @abstractmethod
    def send_command(self, command: Command):
        """Send command.

        Args:
            command (Command): command received
        """
