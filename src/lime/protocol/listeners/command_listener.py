from abc import ABC
from src.lime.protocol import Command


class CommandListener(ABC):
    """Command listener callback."""

    def on_listener(self, command: Command):
        """Handle callback to handle a received command.

        Args:
            command (Command): the received command
        """
        pass
