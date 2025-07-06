from application.models.enums.notification_medium import NotificationMedium
from application.models.enums.notification_types import NotificationTypes
from application.models.enums.notification_status import NotificationStatus
from datetime import datetime

class NotificationDto:
    """
    Notification Data Structure
    """
    def __init__(self, user_id: str, 
                 notification_medium: NotificationMedium, 
                 notification_type: NotificationTypes, 
                 message: str, 
                 status: NotificationStatus = NotificationStatus.UNDELIVERED, 
                 sent_datetime: datetime | None = None):
        """
        Initializes the Notification.

        :param user_id: The unique identifier for the user receiving the notification.
        :param notification_type: The type of the notification (e.g., 'LeeValleyTennisBookingReminder' etc.).
        :param notification_medium: The medium used for transmission of notification (e.g., 'whatsapp', 'email', etc.).
        :param message: The message to be sent in the notification.
        :param status: The status of the notification (e.g., 'sent', 'failed').
        :param sent_datetime: The date and time when the notification was sent. Defaults to None.

        """
        if not isinstance(user_id, str):
            raise ValueError("user_id must be a string")
        self.user_id = user_id

        if not isinstance(notification_type, NotificationTypes):
            raise ValueError("notification_type must be an instance of NotificationTypes")
        self.notification_type = notification_type

        if not isinstance(notification_medium, NotificationMedium):
            raise ValueError("notification_medium must be an instance of NotificationMedium")
        self.notification_medium = notification_medium

        if not isinstance(message, str):
            raise ValueError("message must be a string")
        self.message = message

        if not isinstance(status, NotificationStatus):
            raise ValueError("status must be an instance of NotificationStatus")
        self.status = status

        if sent_datetime is not None and not isinstance(sent_datetime, datetime):
            raise ValueError("sent_datetime must be a datetime instance or None")
        self.sent_datetime = sent_datetime

    def __eq__(self, other):
        if not isinstance(other, NotificationDto):
            return NotImplemented
        return (self.user_id == other.user_id and
                self.notification_type == other.notification_type and
                self.notification_medium == other.notification_medium and
                self.message == other.message and
                self.status == other.status and
                self.sent_datetime == other.sent_datetime)