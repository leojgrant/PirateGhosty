from application.models.enums.adapter_operation_status import AdapterOperationStatus

class DeleteNotificationHistoryResponse:
    """
    Delete Notifications History Response Structure
    """
    def __init__(self, status: AdapterOperationStatus, message: str):
        """
        Initializes the Delete Notification Response.

        :param status: The status of the notification (e.g., 'success', 'failed').
        :param message: A verbose message about the success or failure of the operation.
        """
        if not isinstance(status, AdapterOperationStatus):
            raise ValueError("status must be AdapterOperationStatus.SUCCESS, AdapterOperationStatus.FAILED")
        self.status = status

        if not isinstance(message, str):
            raise ValueError("message must be a string")
        self.message = message      