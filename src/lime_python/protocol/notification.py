from .envelope import Envelope
from .reason import Reason


class Notification(Envelope):
    """Notification representation."""

    def __init__(
        self,
        event: str = None,
        reason: Reason = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.event = event
        self.reason = reason
