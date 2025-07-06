class NotificationHistoryTableEntity:
    """
    Notification History Table Entity Data Structure
    """
    def __init__(self, PartitionKey: str, RowKey: str, user_id: str, notification_type: str, notification_medium: str, message: str, sent_datetime: str, status: str):
        """
        Initializes the Notification History Table Entity.

        :param PartitionKey: The PartitionKey of the entity.
        :param RowKey: The RowKey of the entity.
        :param user_id: The unique identifier for the user associated with the entity.
        :param notification_type: The type of the notification.
        :param notification_medium: The medium through which the notification was sent.
        :param message: The content of the notification message.
        :param sent_datetime: The date and time when the notification was sent.
        :param status: The status of the notification (e.g., sent, failed).
        """
        self.PartitionKey = PartitionKey
        self.RowKey = RowKey
        self.user_id = user_id
        self.notification_type = notification_type
        self.notification_medium = notification_medium
        self.message = message
        self.sent_datetime = sent_datetime
        self.status = status

    def __eq__(self, other):
        if not isinstance(other, NotificationHistoryTableEntity):
            return NotImplemented
        return (self.PartitionKey == other.PartitionKey and
                self.RowKey == other.RowKey and
                self.user_id == other.user_id and
                self.notification_type == other.notification_type and
                self.notification_medium == other.notification_medium and
                self.message == other.message and
                self.sent_datetime == other.sent_datetime and
                self.status == other.status)
