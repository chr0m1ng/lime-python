from abc import ABC

from .reason import Reason
from .serializable import Serializable


class Notification(ABC, Serializable):
    """Notification representation."""

    def __init__(self, event: str, reason: Reason = None):
        self.event = event
        self.reason = reason
