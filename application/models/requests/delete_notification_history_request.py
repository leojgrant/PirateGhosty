from application.models.enums.notification_types import NotificationTypes
from application.models.enums.notification_medium import NotificationMedium
from application.models.enums.notification_status import NotificationStatus
from application.services.utilities.input_validation_service import InputValidationService
from datetime import datetime

class DeleteNotificationHistoryRequest:
    """
    Get Notification History Request Structure
    """
    def __init__(self, user_id: str | None = None, 
                 notification_type: NotificationTypes | None = None,
                 notification_medium: NotificationMedium | None = None,
                 start_date: datetime | None = None,
                 end_date: datetime | None = None,
                 status: NotificationStatus | None = None):
        """
        Deletes the Notification History.

        :param user_id: The unique identifier for the user receiving the notification.
        :param notification_type: The type of the notification (e.g., 'LeeValleyTennisBookingReminder' etc.).
        :param notification_medium: The medium used for transmission of notification (e.g., 'whatsapp', 'email', etc.).
        :param start_date: The start date for filtering notifications.
        :param end_date: The end date for filtering notifications.
        :param status: The status of the notification (e.g., 'sent', 'failed').
        """
        if user_id is not None and not isinstance(user_id, str) and InputValidationService.is_valid_uuid(user_id):
            raise ValueError("user_id must be a string and valid UUID")
        self.user_id = user_id

        if notification_type is not None and not isinstance(notification_type, NotificationTypes):
            raise ValueError("notification_type must be an instance of NotificationTypes")
        self.notification_type = notification_type

        if notification_medium is not None and not isinstance(notification_medium, NotificationMedium):
            raise ValueError("notification_medium must be an instance of NotificationMedium")
        self.notification_medium = notification_medium

        if start_date is not None and not isinstance(start_date, datetime):
            raise ValueError("start_date must be a datetime instance")
        self.start_date = start_date

        if end_date is not None and not isinstance(end_date, datetime):
            raise ValueError("end_date must be a datetime instance")
        self.end_date = end_date

        if status is not None and not isinstance(status, NotificationStatus):
            raise ValueError("status must be an instance of NotificationStatus")
        self.status = status