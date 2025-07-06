from application.models.dtos.notification_dto import NotificationDto
from application.models.enums.adapter_operation_status import AdapterOperationStatus

class StoreNotificationHistoryResponse:
    """
    Store Notification History Response Structure
    """
    def __init__(self, notification: NotificationDto, status: AdapterOperationStatus, message: str):
        """
        Initializes the Store Notification History Response.

        :param notification: The notification that was added to the history.
        :param status: The status of the notification (e.g., 'success', 'failed').
        :param message: A verbose message about the notification status.
        """
        if not isinstance(notification, NotificationDto):
            raise ValueError("notification must be an instance of NotificationDto")
        self.notification = notification

        if not isinstance(status, AdapterOperationStatus):
            raise ValueError("status must be AdapterOperationStatus.SUCCESS, AdapterOperationStatus.FAILED")
        self.status = status
        
        if not isinstance(message, str):
            raise ValueError("message must be a string")
        self.message = message      