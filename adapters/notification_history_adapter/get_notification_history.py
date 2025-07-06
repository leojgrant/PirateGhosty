from connectors.azure_table_connector.azure_table_connector import AzureTableConnector
from adapters.notification_history_adapter.models.notification_history_table_entity import NotificationHistoryTableEntity
from adapters.notification_history_adapter.notification_history_adapter_config import NotificationHistoryAdapterConfig
from application.models.responses.store_notification_history_response import StoreNotificationHistoryResponse
from application.models.dtos.notification_dto import NotificationDto
from application.models.enums.adapter_operation_status import AdapterOperationStatus
from application.models.enums.notification_types import NotificationTypes
from application.models.enums.notification_medium import NotificationMedium
from application.models.enums.notification_status import NotificationStatus
from application.models.responses.get_notification_history_response import GetNotificationHistoryResponse
from application.models.requests.get_notification_history_request import GetNotificationHistoryRequest
from application.services.utilities.input_validation_service import InputValidationService
import logging
from datetime import datetime

class GetNotificationHistory:
    """
    Adapter for getting notification history data.
    """

    def __init__(self, connector: AzureTableConnector, config: NotificationHistoryAdapterConfig):
        self.connector = connector
        self.table_name = config.notification_history_table_name
    
    def get_notification_history(self, request: GetNotificationHistoryRequest) -> GetNotificationHistoryResponse:
        """
        Get the notification history.
        """
        try:
            logging.info(f"Getting notification to history (notification request: {request.__dict__}).")
            request = self.__private_sanitize_notification_history_request(request)
            query_filter = self.__private_construct_filter_string(request)
            notifications = self.connector.get_entities(table_name=self.table_name, query_filter=query_filter)
            notificationEntities = [NotificationHistoryTableEntity(**n) for n in notifications]
            notificationDtos = self.__private_map_entities_to_dtos(notificationEntities)
            return GetNotificationHistoryResponse(
                notifications=notificationDtos,
                message=f"Successfully queried the notification history table.",
                status=AdapterOperationStatus.SUCCESS
            )    
        except Exception as e:
            logging.error(f"Failed to get notification history (notification history request: {request.__dict__}) with error: {e}")
            return GetNotificationHistoryResponse(
                notifications=[],
                message=f"Failed to get notification history: {str(e)}",
                status=AdapterOperationStatus.FAILED
            )
        
    def __private_construct_filter_string(self, request: GetNotificationHistoryRequest) -> str:
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


    def __private_sanitize_notification_history_request(self, request: GetNotificationHistoryRequest) -> GetNotificationHistoryRequest:
        """
        Sanitize the request to ensure it has the correct format.
        """
        if not isinstance(request, GetNotificationHistoryRequest):
            raise ValueError("__private_sanitize_notification_history_request failed: request must be of type GetNotificationHistoryRequest")
        return request
     

    def  __private_map_entities_to_dtos(self, notification_history_entities: list[NotificationHistoryTableEntity]) -> list[NotificationDto]:
        """
        Map the entities to DTOs
        """
        dtos = []
        for entity in notification_history_entities:
            dtos.append(
                NotificationDto(
                    user_id=entity.user_id,
                    notification_type=NotificationTypes(entity.notification_type),
                    notification_medium=NotificationMedium(entity.notification_medium),
                    message=entity.message,
                    sent_datetime=datetime.strptime(entity.sent_datetime, "%Y-%m-%d %H:%M:%S"),
                    status=NotificationStatus(entity.status)
                )
            )
        return dtos
    