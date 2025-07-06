from application.models.dtos.notification_dto import NotificationDto
from application.models.enums.adapter_operation_status import AdapterOperationStatus

class GetNotificationHistoryResponse:
    """
    Get Notification History Response Structure
    """
    def __init__(self, notifications: list[NotificationDto], status: AdapterOperationStatus, message: str):
        """
        Initializes the Get Notification Response.

        :param notification: The past notifications.
        :param status: The status of the notification (e.g., 'success', 'failed').
        :param message: A verbose message about the success or failure of the operation.
        """
        if isinstance(notifications, list):
            for notification in notifications:
                if not isinstance(notification, NotificationDto):
                    raise ValueError("Each item in notifications must be an instance of NotificationDto")
        else:
            raise ValueError("notifications must be a list of NotificationDto instances")
        self.notifications = notifications

        if not isinstance(status, AdapterOperationStatus):
            raise ValueError("status must be AdapterOperationStatus.SUCCESS, AdapterOperationStatus.FAILED")
        self.status = status

        if not isinstance(message, str):
            raise ValueError("message must be a string")
        self.message = message      