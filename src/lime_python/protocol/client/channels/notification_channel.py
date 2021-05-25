from abc import abstractmethod

from ...listeners import NotificationListener
from ...notification import Notification


class NotificationChannel(NotificationListener):
    """Notification Channel."""

    @abstractmethod
    def send_notification(self, notification: Notification) -> None:
        """Send a Notification.

        Args:
            notification (Notification): Notification to be sent
        """
        pass
