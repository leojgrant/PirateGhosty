from abc import ABC, abstractmethod

class WhatsappNotificationsAdapterConfig(ABC):
    """
    Configuration class for the Whatsapp Notifications Adapter.
    """

    # The Twilio account SID for sending notifications.
    @property
    @abstractmethod
    def twilio_account_sid(self) -> str:
        pass

    # The Twilio authentication token for sending notifications.
    @property
    @abstractmethod
    def twilio_auth_token(self) -> str:
        pass

    # The phone number to be used for sending WhatsApp messages via Twilio.
    @property
    @abstractmethod
    def twilio_whatsapp_number(self) -> str:
        pass
