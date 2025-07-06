from adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter_config import NotificationsAdapterConfig
from connectors.azure_table_connector.azure_table_connector_config import AzureTableConnectorConfig
from adapters.secrets_adapter.secrets_adapter import SecretsAdapter, SecretsAdapterConfig
from dotenv import load_dotenv
import os


load_dotenv() 

class AppConfig(AzureTableConnectorConfig, NotificationsAdapterConfig):
    """
    Configuration class for the application.
    """
    def __init__(self, *args, **kwargs):
        super().__init__()

### Construct the application configuration
secrets_adapter_config = SecretsAdapterConfig(os.getenv("KEYVAULT_URL"))
secrets_adapter = SecretsAdapter(secrets_adapter_config)

app_config = AppConfig(
    azure_table_connection_string=secrets_adapter.get_secret("AzureTableConnectionString"),
    twilio_account_sid=secrets_adapter.get_secret("TwilioAccountSID"),
    twilio_auth_token=secrets_adapter.get_secret("TwilioAuthToken"),
    twilio_whatsapp_number=secrets_adapter.get_secret("TwilioWhatsAppNumber"),
)