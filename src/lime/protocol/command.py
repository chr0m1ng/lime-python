from abc import ABC
from .command_method import CommandMethod
from .command_status import CommandStatus
from .envelope import Envelope
from .reason import Reason


class Command(ABC, Envelope):  # noqa: WPS230
    """Envelope representation."""

    def __init__(
        self,
        uri: str = None,
        type_n: str = None,
        resource: str = None,
        method: CommandMethod = None,
        status: CommandStatus = None,
        reason: Reason = None,
        timeout: bool = None
    ):

        self.uri = uri
        self.type_n = type_n
        self.resource = resource
        self.method = method
        self.status = status
        self.reason = reason
        self.timeout = timeout


class CommandListener(ABC):
    """Command listener callback."""

    def on_listener(self, command: Command):
        """Handle callback to handle a received command.

        Args:
            command (Command): the received command
        """
        pass
