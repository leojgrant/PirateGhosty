from abc import ABC, abstractmethod

class AzureTableConnectorConfig(ABC):
    """
    Configuration class for the Azure Table Connector.
    """

    def __init__(self, azure_table_connection_string: str):
        """
        Initialize the Azure Table Connector with the provided configuration settings.

        Args:
            azure_table_connection_string (str): The connection string for the Azure Storage account.
        """
        self.azure_table_connection_string = azure_table_connection_string
