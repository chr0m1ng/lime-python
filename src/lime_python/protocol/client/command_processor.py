from abc import abstractmethod

from ..command import Command
from ..listeners import CommandListener


class CommandProcessor(CommandListener):
    """Command Processor."""

    @abstractmethod
    async def process_command_async(
        self,
        command: Command,
        timeout: float
    ) -> Command:
        """Process a Command asynchronously and return the result.

        Args:
            command (Command): The Command to be processed
            timeout (float): Timeout to process the Command

        Returns:
            Command: The result Command
        """  # noqa: DAR202
        pass
