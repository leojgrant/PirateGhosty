from connectors.azure_table_connector.azure_table_connector import AzureTableConnector
from adapters.notification_history_adapter.models.notification_history_table_entity import NotificationHistoryTableEntity
from adapters.notification_history_adapter.notification_history_adapter_config import NotificationHistoryAdapterConfig
from application.models.responses.store_notification_history_response import StoreNotificationHistoryResponse
from application.models.enums.adapter_operation_status import AdapterOperationStatus
from application.models.requests.store_notification_history_request import StoreNotificationHistoryRequest
import logging

class StoreNotificationHistory:
    """
    Adapter for Notification History
    """

    def __init__(self, connector: AzureTableConnector, config: NotificationHistoryAdapterConfig):
        self.connector = connector
        self.table_name = config.notification_history_table_name
    ### Should be in service layer, not adapter layer
    # def get_booking_date_of_latest_notification(self, user_id: str) -> int:
    #     """
    #     Get the booking date of the most recent notification sent to a user.
    #     """
    #     row_key = self.connector.get_number_of_rows_in_partition(table_name=self.table_name, partition_key=user_id) - 1
    #     if row_key == -1:
    #         return 0 # return 0 if no notifications exist
    #     entity = self.connector.get_entity(table_name=self.table_name, partition_key=user_id, row_key=row_key)
    #     return entity["BookingDate"]
    
    def store_notification_history(self, request: StoreNotificationHistoryRequest) -> StoreNotificationHistoryResponse:
        """
        Add a notification to the history.
        """
        try:
            logging.info(f"Adding notification to history (notification: {request.__dict__}).")
            partition_key = request.notification.user_id
            row_key = str(self.connector.get_number_of_rows_in_partition(table_name=self.table_name, partition_key=partition_key))
            entity = NotificationHistoryTableEntity(PartitionKey=partition_key, 
                                                    RowKey=row_key, 
                                                    user_id=request.notification.user_id, 
                                                    notification_type=request.notification.notification_type.value,
                                                    notification_medium=request.notification.notification_medium.value,
                                                    message=request.notification.message,
                                                    sent_datetime=request.notification.sent_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                                    status=request.notification.status.value)
            self.connector.insert_entity(table_name=self.table_name, entity=entity.__dict__)
            return StoreNotificationHistoryResponse(
                notification=request.notification,
                message=f"Successfully added notification to notification history table.",
                status=AdapterOperationStatus.SUCCESS
            )    
        except Exception as e:
            logging.error(f"Failed to add notification to history (notification: {request.notification.__dict__}) with error: {e}")
            return StoreNotificationHistoryResponse(
                notification=request.notification,
                message=f"Failed to add notification to history: {str(e)}",
                status=AdapterOperationStatus.FAILED
            )       

    # def  __private_map_entities_to_dtos(self, notification_history_entities: list[NotificationHistoryTableEntity]) -> list[NotificationHistoryDto]:
    #     """
    #     Map the entities to DTOs
    #     """
    #     user_settings = []
    #     for entity in notification_history_entities:
    #         user_settings.append(
    #             NotificationHistoryDto(
    #                 notification=NotificationDto(
    #                     user_id=entity.PartitionKey,
    #                     notification_type=NotificationTypes(entity.notification_type),
    #                     notification_medium=NotificationMedium(entity.notification_medium),
    #                     message=entity.message
    #                 ),
    #                 sent_datetime=datetime.strptime(entity.sent_datetime, "%Y-%m-%d %H:%M:%S"),
    #                 status=NotificationStatus(entity.status)
    #             )
    #         )
    #     return user_settings