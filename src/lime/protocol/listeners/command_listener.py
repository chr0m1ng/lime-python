from abc import ABC, abstractmethod

from ..command import Command


class CommandListener(ABC):
    """Command listener callback."""

    @abstractmethod
    def on_command(self, command: Command) -> None:
        """Handle callback to handle a received command.

        Args:
            command (Command): the received Command
        """
        pass
