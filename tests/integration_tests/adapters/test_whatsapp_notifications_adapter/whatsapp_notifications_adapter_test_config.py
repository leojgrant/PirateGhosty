from abc import abstractmethod
from adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter import WhatsappNotificationsAdapterConfig

class WhatsappNotificationsAdapterTestConfig(WhatsappNotificationsAdapterConfig):
    """
    Configuration class for the Notifications Adapter Test.
    """

    # The whatsapp number to be used for testing purposes.
    @property
    @abstractmethod
    def test_target_whatsapp_number(self) -> str:
        pass
