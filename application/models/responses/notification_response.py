from application.models.enums.notification_status import NotificationStatus

class NotificationResponse:
    """
    Notification Response Structure
    """
    def __init__(self, user_id: str, status: NotificationStatus, message: str):
        """
        Initializes the Notification.

        :param user_id: The unique identifier for the user associated with the notification.
        :param status: The status of the notification (e.g., 'queued', 'sent', 'delivered', 'failed').
        :param message: A verbose message about the notification status.
        """
        self.user_id = user_id
        if not isinstance(status, NotificationStatus):
            raise ValueError("status must be NotificationStatus.QUEUED, NotificationStatus.SENT, NotificationStatus.DELIVERED or NotificationStatus.FAILED")
        self.status = status
        self.message = message      