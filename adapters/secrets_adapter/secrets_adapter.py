from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from adapters.secrets_adapter.secrets_adapter_config import SecretsAdapterConfig

class SecretsAdapter:
    """
    This class is responsible for managing secrets in the application.
    It provides methods to get secrets.
    """

    def __init__(self, secretsAdapterConfig: SecretsAdapterConfig):
        self.secret_client = SecretClient(
            vault_url=secretsAdapterConfig.keyvault_url,
            credential=DefaultAzureCredential(),
        )

    def get_secret(self, secret_name: str) -> str:
        """
        Get a secret by its name.

        :param secret_name: The name of the secret to retrieve.
        :return: The value of the secret.
        """
        return self.secret_client.get_secret(secret_name).value
