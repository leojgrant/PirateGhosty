from abc import ABC, abstractmethod

class NotificationHistoryAdapterConfig(ABC):
    """
    Configuration class for the Notification History Adapter.
    """

    # The table name in the Azure Table Storage where notification history is stored.
    @property
    @abstractmethod
    def notification_history_table_name(self) -> str:
        pass

