from abc import ABC, abstractmethod

from ..notification import Notification


class NotificationListener(ABC):
    """Notification listener callback."""

    @abstractmethod
    def on_notification(self, notification: Notification) -> None:
        """Handle callback to handle a received notification.

        Args:
            notification (Notification): the received Notification
        """
        pass
