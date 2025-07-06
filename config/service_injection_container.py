from dependency_injector import containers, providers
from connectors.azure_table_connector.azure_table_connector import AzureTableConnector
from adapters.notification_history_adapter.store_notification_history import StoreNotificationHistory
import config.app_config as app_config

class ServiceInjectionContainer(containers.DeclarativeContainer):
    # CONNECTORS
    azure_table_connector = providers.Singleton(
        AzureTableConnector,
        azureTableConnectorConfig=app_config.app_config
    )

    # ADAPTERS
    # notification_history_adapter = providers.Singleton(
    #     StoreNotificationHistory,
    #     connector=azure_table_connector,
    # )


    # SERVICES

    