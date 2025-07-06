import pytest
import datetime
from unittest.mock import patch, MagicMock
from application.models.dtos.notification_dto import NotificationDto
from application.models.enums.notification_status import NotificationStatus
from tests.unit_tests.unit_test_config import unit_test_config
from application.models.enums.notification_medium import NotificationMedium
from application.models.enums.notification_types import NotificationTypes
from adapters.notification_history_adapter.store_notification_history import StoreNotificationHistory
from adapters.notification_history_adapter.notification_history_adapter_config import NotificationHistoryAdapterConfig
from adapters.notification_history_adapter.models.notification_history_table_entity import NotificationHistoryTableEntity
from application.models.requests.store_notification_history_request import StoreNotificationHistoryRequest
from application.models.enums.adapter_operation_status import AdapterOperationStatus
from application.models.responses.store_notification_history_response import StoreNotificationHistoryResponse

####################### MOCKS #######################

@pytest.fixture(scope='module')
def mock_notification_history_adapter_config(unit_test_config):
    unit_test_config.notification_history_table_name = 'NotificationHistoryTestTable'
    return unit_test_config

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

@patch('adapters.notification_history_adapter.store_notification_history.AzureTableConnector') 
def test_store_notification_history_success(mock_azure_table_connector_class: MagicMock, 
                                   mock_notification_history_adapter_config: NotificationHistoryAdapterConfig, 
                                   mock_store_notification_history_request: StoreNotificationHistoryRequest):
    
    # Arrange
    mock_azure_table_connector = MagicMock() 
    mock_azure_table_connector.get_number_of_rows_in_partition.return_value = "0"
    mock_azure_table_connector_class.return_value = mock_azure_table_connector
    adapter = StoreNotificationHistory(mock_azure_table_connector, mock_notification_history_adapter_config)
    notification = mock_store_notification_history_request.notification
    expected_stored_entity = NotificationHistoryTableEntity(PartitionKey=notification.user_id, 
                                            RowKey="0", 
                                            user_id=notification.user_id, 
                                            notification_type=notification.notification_type.value,
                                            notification_medium=notification.notification_medium.value,
                                            message=notification.message,
                                            sent_datetime=notification.sent_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                            status=notification.status.value)

    # Act
    response = adapter.store_notification_history(mock_store_notification_history_request)

    # Assert
    mock_azure_table_connector.insert_entity.assert_called_once()
    mock_azure_table_connector.insert_entity.assert_called_once_with(
        table_name=mock_notification_history_adapter_config.notification_history_table_name,
        entity=expected_stored_entity.__dict__
    )
    assert isinstance(response, StoreNotificationHistoryResponse)
    assert response.status == AdapterOperationStatus.SUCCESS
    


@patch('adapters.notification_history_adapter.store_notification_history.AzureTableConnector')
def test_send_notification_logs_error_on_exception(mock_azure_table_connector_class: MagicMock, 
                                                   mock_notification_history_adapter_config: NotificationHistoryAdapterConfig, 
                                                   mock_store_notification_history_request: StoreNotificationHistoryRequest,
                                                   caplog: pytest.LogCaptureFixture):
    # Arrange
    mock_azure_table_connector = MagicMock() 
    mock_azure_table_connector.get_number_of_rows_in_partition.return_value = "0"
    mock_azure_table_connector.insert_entity.side_effect = Exception("Failed to store entity")
    mock_azure_table_connector_class.return_value = mock_azure_table_connector
    adapter = StoreNotificationHistory(mock_azure_table_connector, mock_notification_history_adapter_config)

    # Act
    with caplog.at_level('ERROR'):
        response = adapter.store_notification_history(mock_store_notification_history_request)

    # Assert
    assert "Failed to add notification to history (notification: {'user_id': '123e4567-e89b-12d3-a456-426614174000', 'notification_type': <NotificationTypes.LEE_VALLEY_TENNIS_BOOKING_ALERT: 'lee_valley_tennis_booking_alert'>, 'notification_medium': <NotificationMedium.WHATSAPP: 'whatsapp'>, 'message': 'Test notification for 123e4567-e89b-12d3-a456-426614174000', 'status': <NotificationStatus.SENT: 'sent'>, 'sent_datetime': datetime.datetime(2025, 3, 13, 7, 30)}) with error: Failed to store entity" in caplog.text
    assert isinstance(response, StoreNotificationHistoryResponse)
    assert response.status == AdapterOperationStatus.FAILED 


