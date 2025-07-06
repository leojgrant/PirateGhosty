from adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter import WhatsappNotificationsAdapterConfig
from adapters.notification_history_adapter.notification_history_adapter_config import NotificationHistoryAdapterConfig
import pytest
from copy import deepcopy

class UnitTestConfig(WhatsappNotificationsAdapterConfig, NotificationHistoryAdapterConfig):
    """
    Configuration class for the Unit Tests.
    """
    def __init__(self, 
                 twilio_account_sid: str, 
                 twilio_auth_token: str, 
                 twilio_whatsapp_number: str,
                 notification_history_table_name: str,):
        self._twilio_account_sid = twilio_account_sid
        self._twilio_auth_token = twilio_auth_token
        self._twilio_whatsapp_number = twilio_whatsapp_number
        self._notification_history_table_name = notification_history_table_name

    @property
    def twilio_account_sid(self) -> str:
        return self._twilio_account_sid
    
    @twilio_account_sid.setter
    def twilio_account_sid(self, value: str):
        self._twilio_account_sid = value

    @property
    def twilio_auth_token(self) -> str:
        return self._twilio_auth_token
    
    @twilio_auth_token.setter
    def twilio_auth_token(self, value: str):
        self._twilio_auth_token = value

    @property
    def twilio_whatsapp_number(self) -> str:
        return self._twilio_whatsapp_number
    
    @twilio_whatsapp_number.setter
    def twilio_whatsapp_number(self, value: str):
        self._twilio_whatsapp_number = value

    @property
    def notification_history_table_name(self) -> str:
        return self._notification_history_table_name
    
    @notification_history_table_name.setter
    def notification_history_table_name(self, value: str):
        self._notification_history_table_name = value

config = UnitTestConfig(
        twilio_account_sid="ReplaceMeInTesting",
        twilio_auth_token="ReplaceMeInTesting",
        twilio_whatsapp_number="ReplaceMeInTesting",
        notification_history_table_name="ReplaceMeInTesting",
    )

@pytest.fixture(scope="session")
def unit_test_config():
    return deepcopy(config)