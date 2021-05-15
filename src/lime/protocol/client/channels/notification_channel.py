from ...listeners import NotificationListener
from ...notification import Notification


class NotificationChannel(NotificationListener):
    """Notification Channel."""

    def send_notification(self, notification: Notification):
        """Send a Notification.

        Args:
            notification (Notification): Notification to be sent
        """
        pass
