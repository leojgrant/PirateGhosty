from application.models.dtos.notification_dto import NotificationDto

class StoreNotificationHistoryRequest:
    """
    Store Notification History Request Structure
    """
    def __init__(self, notification: NotificationDto):
        """
        Initializes the Notification.

        :param notification: The notification to be stored.
        """
        if not isinstance(notification, NotificationDto):
            raise ValueError("notification must be an instance of NotificationDto")
        self.notification = notification