from abc import ABC
from ..notification import Notification


class NotificationListener(ABC):
    """Notification listener callback."""

    def on_notification(self, notification: Notification):
        """Handle callback to handle a received notification.

        Args:
            notification (Notification): the received Notification
        """
        pass
