from application.models.enums.notification_status import NotificationStatus
from application.models.dtos.notification_dto import NotificationDto

class WhatsappNotificationRequest:
    """
    WhatsApp Notification Request Structure
    """
    def __init__(self, notification: NotificationDto, phone_number: str):
        """
        Initializes the Notification.

        :param notification: The notification to be sent.
        :param phone_number: The phone number to which the notification will be sent.
        """
        if not isinstance(notification, NotificationDto):
            raise ValueError("notification must be an instance of NotificationDto")
        self.notification = notification

        if not isinstance(phone_number, str):
            raise ValueError("phone_number must be a string")
        self.phone_number = phone_number 