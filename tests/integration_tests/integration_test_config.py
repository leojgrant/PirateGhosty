from tests.integration_tests.adapters.test_whatsapp_notifications_adapter.whatsapp_notifications_adapter_test_config import WhatsappNotificationsAdapterTestConfig
from connectors.azure_table_connector.azure_table_connector_config import AzureTableConnectorConfig
from adapters.secrets_adapter.secrets_adapter import SecretsAdapter, SecretsAdapterConfig
from adapters.notification_history_adapter.notification_history_adapter_config import NotificationHistoryAdapterConfig
from connectors.azure_table_connector.azure_table_connector import AzureTableConnector
import os
import pytest
from copy import deepcopy
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class IntegrationTestConfig(AzureTableConnectorConfig, WhatsappNotificationsAdapterTestConfig, NotificationHistoryAdapterConfig):
    """
    Configuration class for the Integration Tests.
    """
    def __init__(self, 
                 azure_table_connection_string: str,
                 twilio_account_sid: str, 
                 twilio_auth_token: str, 
                 twilio_whatsapp_number: str,
                 test_target_whatsapp_number: str,
                 notification_history_table_name: str):
        self._azure_table_connection_string = azure_table_connection_string
        self._twilio_account_sid = twilio_account_sid
        self._twilio_auth_token = twilio_auth_token
        self._twilio_whatsapp_number = twilio_whatsapp_number
        self._test_target_whatsapp_number = test_target_whatsapp_number
        self._notification_history_table_name = notification_history_table_name

    @property
    def azure_table_connection_string(self) -> str:
        return self._azure_table_connection_string
    
    @azure_table_connection_string.setter
    def azure_table_connection_string(self, value: str):
        self._azure_table_connection_string = value

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
    def test_target_whatsapp_number(self) -> str:
        return self._test_target_whatsapp_number
    
    @test_target_whatsapp_number.setter
    def test_target_whatsapp_number(self, value: str):
        self._test_target_whatsapp_number = value

    @property
    def notification_history_table_name(self) -> str:
        return self._notification_history_table_name
    
    @notification_history_table_name.setter
    def notification_history_table_name(self, value: str):
        self._notification_history_table_name = value

    def get_copy(self):
        """
        Returns a deep copy of the current configuration instance.
        """
        return deepcopy(self)

### Construct the application configuration
secrets_adapter_config = SecretsAdapterConfig(os.getenv("KEYVAULT_URL"))
secrets_adapter = SecretsAdapter(secrets_adapter_config)

config = IntegrationTestConfig(
        azure_table_connection_string=secrets_adapter.get_secret("AzureTableConnectionString"),
        twilio_account_sid=secrets_adapter.get_secret("TwilioAccountSID"),
        twilio_auth_token=secrets_adapter.get_secret("TwilioAuthToken"),
        twilio_whatsapp_number=secrets_adapter.get_secret("TwilioWhatsAppNumber"),
        test_target_whatsapp_number=secrets_adapter.get_secret("TestTargetWhatsAppNumber"),
        notification_history_table_name="NotificationHistoryTestTable",
    )

@pytest.fixture(scope="session")
def integration_test_config():
    return config.get_copy()  # Return a copy to avoid modifying the original config during tests


### Singleton dependencies for the integration tests
azure_table_connector_singleton_instance = None

@pytest.fixture(scope="session")
def azure_table_connector(integration_test_config):
    global azure_table_connector_singleton_instance
    if azure_table_connector_singleton_instance is None:
        azure_table_connector_singleton_instance = AzureTableConnector(
            azure_table_connector_config=integration_test_config
        )
    yield azure_table_connector_singleton_instance