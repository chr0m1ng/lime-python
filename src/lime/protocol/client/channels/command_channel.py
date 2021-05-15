from ...command import Command
from ...listeners import CommandListener


class CommandChannel(CommandListener):
    """Command Channel."""

    def send_command(self, command: Command):
        """Send a Command.

        Args:
            command (Command): Command to be sent
        """
        pass
