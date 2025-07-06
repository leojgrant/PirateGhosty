from azure.data.tables import TableServiceClient, TableClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from connectors.azure_table_connector.azure_table_connector_config import AzureTableConnectorConfig

class AzureTableConnector:
    def __init__(self, azure_table_connector_config: AzureTableConnectorConfig):
        """
        Initializes the Azure Table Connector.

        :param azure_table_connector_config: Azure Storage account configuration settings.
        """
        self.service_client = TableServiceClient.from_connection_string(azure_table_connector_config.azure_table_connection_string) 

    def _get_table_client(self, table_name: str) -> TableClient:
        """
        Returns the table client.

        :return: TableClient instance.
        """
        return self.service_client.create_table_if_not_exists(table_name)

    def insert_entity(self, table_name: str, entity: dict) -> None:
        """
        Inserts an entity into the Azure Table.

        :param entity: A dictionary representing the entity to insert.
        """
        try:
            print(f"Inserting entity: {entity}")
            table_client = self._get_table_client(table_name)
            table_client.create_entity(entity)
        except ResourceExistsError:
            raise ValueError("Entity with the same PartitionKey and RowKey already exists.")

    def get_entity(self, table_name: str, partition_key: str, row_key: int) -> dict:
        """
        Retrieves an entity from the Azure Table.

        :param partition_key: The PartitionKey of the entity.
        :param row_key: The RowKey of the entity.
        :return: A dictionary representing the entity.
        """
        try:
            table_client = self._get_table_client(table_name)
            return table_client.get_entity(partition_key, row_key)
        except ResourceNotFoundError:
            raise ValueError("Entity not found.")
        
    def get_entities_by_partition_key(self, table_name: str, partition_key: str) -> list:
        """
        Retrieves all entities from a given partition.

        :param partition_key: The PartitionKey to filter entities by.
        :return: A list of dictionaries representing the entities.
        """
        table_client = self._get_table_client(table_name)
        query_filter = f"PartitionKey eq '{partition_key}'"
        entities = table_client.query_entities(query_filter)
        return [entity for entity in entities]
    
    def get_entities(self, table_name: str, query_filter: str) -> list:
        """
        Retrieves all entities from a given partition.

        :param table_name: The name of the Azure Table.
        :param query_filter: The OData filter string to apply to the query.
        :return: A list of dictionaries representing the entities.
        """
        table_client = self._get_table_client(table_name)
        entities = table_client.query_entities(query_filter)
        yielded_entities = [entity for entity in entities]
        return yielded_entities

    def get_all_entities(self, table_name: str) -> list:
        """
        Retrieves all entities from the Azure Table.

        :return: A list of dictionaries representing all entities.
        """
        table_client = self._get_table_client(table_name)
        entities = table_client.list_entities()
        return [entity for entity in entities]
        
    def get_number_of_rows_in_partition(self, table_name: str, partition_key: str) -> int:
        """
        Returns the number of rows in a given partition.

        :param partition_key: The PartitionKey to count rows for.
        :return: The number of rows in the specified partition.
        """
        table_client = self._get_table_client(table_name)
        query_filter = f"PartitionKey eq '{partition_key}'"
        entities = table_client.query_entities(query_filter)
        return sum(1 for _ in entities)
    
    def delete_entity(self, table_name: str, partition_key: str, row_key: int) -> None:
        """
        Deletes an entity from the Azure Table.

        :param table_name: The name of the Azure Table.
        :param partition_key: The PartitionKey of the entity to delete.
        :param row_key: The RowKey of the entity to delete.
        """
        try:
            table_client = self._get_table_client(table_name)
            table_client.delete_entity(partition_key, row_key)
        except ResourceNotFoundError:
            raise ValueError("Entity not found.")
