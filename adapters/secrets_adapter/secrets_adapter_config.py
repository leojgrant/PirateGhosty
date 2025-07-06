class SecretsAdapterConfig:
    """
    Configuration class for the Secrets Adapter.
    """

    def __init__(self, keyvault_url: str):
        """
        Initialize the SecretsAdapterConfig with the provided configuration settings.

        Args:
            keyvault_url (str): The URL of the Azure Key Vault where secrets are stored.
        """
        self.keyvault_url = keyvault_url

