from abc import abstractmethod
from ...listeners import NotificationListener
from ...notification import Notification


class NotificationChannel(NotificationListener):
    """Notification Channel representation."""

    @abstractmethod
    def send_notification(self, notification: Notification):
        """Handle notification channel.

        Args:
            notification (Notification): Notification received
        """
        pass
