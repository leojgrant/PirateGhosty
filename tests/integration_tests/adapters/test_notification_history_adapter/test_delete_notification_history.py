import pytest
import datetime
from tests.integration_tests.integration_test_config import integration_test_config, azure_table_connector
from application.models.dtos.notification_dto import NotificationDto
from application.models.enums.notification_status import NotificationStatus
from application.models.enums.notification_medium import NotificationMedium
from application.models.enums.notification_types import NotificationTypes
from adapters.notification_history_adapter.store_notification_history import StoreNotificationHistory
from adapters.notification_history_adapter.notification_history_adapter_config import NotificationHistoryAdapterConfig
from application.models.requests.store_notification_history_request import StoreNotificationHistoryRequest
from connectors.azure_table_connector.azure_table_connector import AzureTableConnector
from adapters.notification_history_adapter.get_notification_history import GetNotificationHistory
from application.models.requests.get_notification_history_request import GetNotificationHistoryRequest
from adapters.notification_history_adapter.delete_notification_history import DeleteNotificationHistory 
from application.models.requests.delete_notification_history_request import DeleteNotificationHistoryRequest
from application.models.responses.delete_notification_history_response import DeleteNotificationHistoryResponse
from application.models.enums.adapter_operation_status import AdapterOperationStatus


####################### MOCKS #######################

@pytest.fixture(scope='module')
def notification_history_adapter_config(integration_test_config):
        return integration_test_config

@pytest.fixture(scope='module')
def mock_notification():
    return NotificationDto(
        user_id='123e4567-e89b-12d3-a456-426614174000',
        notification_medium=NotificationMedium.WHATSAPP,
        notification_type=NotificationTypes.LEE_VALLEY_TENNIS_BOOKING_ALERT,
        message='Test notification for 123e4567-e89b-12d3-a456-426614174000',
        status=NotificationStatus.SENT,
        sent_datetime=datetime.datetime(2025, 3, 13, 7, 30)
    )

@pytest.fixture(scope='module')
def mock_store_notification_history_request(mock_notification):
    return StoreNotificationHistoryRequest(
        notification = mock_notification,
    )


######################## TESTS #######################

def test_delete_all_notification_history_success(notification_history_adapter_config: NotificationHistoryAdapterConfig,
                                   azure_table_connector: AzureTableConnector,
                                   mock_store_notification_history_request: StoreNotificationHistoryRequest,
                                   mock_notification: NotificationDto):
    
    # Arrange
    delete_notification_history_table = DeleteNotificationHistory(azure_table_connector, notification_history_adapter_config)
    store_notification_history = StoreNotificationHistory(azure_table_connector, notification_history_adapter_config)
    get_notification_history = GetNotificationHistory(azure_table_connector, notification_history_adapter_config)

    # Act
    store_notification_history.store_notification_history(mock_store_notification_history_request)
    stored_notifications_before_deletion = get_notification_history.get_notification_history(GetNotificationHistoryRequest(user_id=mock_notification.user_id)).notifications
    response = delete_notification_history_table.delete_notification_history(DeleteNotificationHistoryRequest())
    stored_notifications_after_deletion = get_notification_history.get_notification_history(GetNotificationHistoryRequest(user_id=mock_notification.user_id)).notifications

    
    # Assert
    assert response.status == AdapterOperationStatus.SUCCESS
    assert response.message == "Successfully deleted notification history."
    assert isinstance(response, DeleteNotificationHistoryResponse)
    assert all(isinstance(n, NotificationDto) for n in stored_notifications_after_deletion)
    assert stored_notifications_before_deletion == [ mock_notification ]
    assert len(stored_notifications_after_deletion) == 0



