from application.models.requests.delete_notification_history_request import DeleteNotificationHistoryRequest
from adapters.notification_history_adapter.notification_history_adapter_config import NotificationHistoryAdapterConfig
from connectors.azure_table_connector.azure_table_connector import AzureTableConnector
from application.models.responses.delete_notification_history_response import DeleteNotificationHistoryResponse
from application.models.enums.adapter_operation_status import AdapterOperationStatus
import logging

class DeleteNotificationHistory:
    """
    Adapter for deleting notification history data.
    """

    def __init__(self, connector: AzureTableConnector, config: NotificationHistoryAdapterConfig):
        self.connector = connector
        self.table_name = config.notification_history_table_name

    def delete_notification_history(self, request: DeleteNotificationHistoryRequest) -> DeleteNotificationHistoryResponse:
        """
        Deletes a notification history entry by its ID.

        Args:
            request (DeleteNotificationHistoryRequest): Request containing the details of the notification history to be deleted.

        Returns:
            DeleteNotificationHistoryResponse: Response indicating the success or failure of the deletion operation.
        """
        try:
            logging.info(f"Deleting notification history (notification request: {request.__dict__}).")

            request = self.__private_sanitize_notification_history_request(request)
            query_filter = self.__private_construct_filter_string(request)
            entities = self.connector.get_entities(table_name=self.table_name, query_filter=query_filter)
            for entity in entities:
                self.connector.delete_entity(table_name=self.table_name, partition_key=entity['PartitionKey'], row_key=entity['RowKey'])
            return DeleteNotificationHistoryResponse(
                message=f"Successfully deleted notification history.",
                status=AdapterOperationStatus.SUCCESS
            )    
        except Exception as e:
            logging.error(f"Failed to delete notification history (notification history request: {request.__dict__}) with error: {e}")
            return DeleteNotificationHistoryResponse(
                message=f"Failed to delete notification history: {str(e)}",
                status=AdapterOperationStatus.FAILED
            )
        
    def __private_sanitize_notification_history_request(self, request: DeleteNotificationHistoryRequest) -> DeleteNotificationHistoryRequest:
        """
        Sanitize the request to ensure it has the correct format.
        """
        if not isinstance(request, DeleteNotificationHistoryRequest):
            raise ValueError("__private_sanitize_notification_history_request failed: request must be of type DeleteNotificationHistoryRequest")
        return request
        
    def __private_construct_filter_string(self, request: DeleteNotificationHistoryRequest) -> str:
        """
        Construct the filter string for querying the notification history.
        """
        filters = []
        if request.user_id:
            filters.append(f"user_id eq '{request.user_id}'")
        if request.notification_medium:
            filters.append(f"notification_medium eq '{request.notification_medium.value}'")
        if request.notification_type:
            filters.append(f"notification_type eq '{request.notification_type.value}'")
        if request.start_date:
            filters.append(f"sent_datetime ge datetime'{request.start_date.strftime('%Y-%m-%d %H:%M:%S')}'")
        if request.end_date:
            filters.append(f"sent_datetime le datetime'{request.end_date.strftime('%Y-%m-%d %H:%M:%S')}'")
        if request.status:
            filters.append(f"status eq '{request.status.value}'")
        
        return " and ".join(filters)