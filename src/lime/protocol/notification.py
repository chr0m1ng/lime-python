from .envelope import Envelope
from .reason import Reason


class Notification(Envelope):
    """Notification representation."""

    def __init__(self, event: str, reason: Reason = None) -> None:
        super().__init__()
        self.event = event
        self.reason = reason
