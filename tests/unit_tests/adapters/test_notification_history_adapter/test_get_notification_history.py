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
from adapters.notification_history_adapter.get_notification_history import GetNotificationHistory
from application.models.requests.get_notification_history_request import GetNotificationHistoryRequest
from application.models.responses.get_notification_history_response import GetNotificationHistoryResponse
import uuid
####################### MOCKS #######################

@pytest.fixture(scope='module')
def mock_notification_history_adapter_config(unit_test_config):
    unit_test_config.notification_history_table_name = 'NotificationHistoryTestTable'
    return unit_test_config

@pytest.fixture(scope='module')
def mock_notification():
    return NotificationDto(
        user_id="123e4567-e89b-12d3-a456-426614174000", 
        notification_medium=NotificationMedium.WHATSAPP,
        notification_type=NotificationTypes.LEE_VALLEY_TENNIS_BOOKING_ALERT,
        message='Test notification for user123',
        status=NotificationStatus.SENT,
        sent_datetime=datetime.datetime(2025, 3, 13, 7, 30)
    )

@pytest.fixture(scope='module')
def mock_get_notification_history_request(mock_notification):
    return GetNotificationHistoryRequest(
       user_id=mock_notification.user_id,
    )


######################## TESTS #######################

@patch('adapters.notification_history_adapter.store_notification_history.AzureTableConnector') 
def test_get_notification_history_success(mock_azure_table_connector_class: MagicMock, 
                                   mock_notification_history_adapter_config: NotificationHistoryAdapterConfig, 
                                   mock_get_notification_history_request: GetNotificationHistoryRequest,
                                   mock_notification: NotificationDto):
    
    # Arrange
    mock_azure_table_connector = MagicMock() 
    stored_entity = NotificationHistoryTableEntity(PartitionKey=mock_notification.user_id, 
                                            RowKey="0", 
                                            user_id=mock_notification.user_id, 
                                            notification_type=mock_notification.notification_type.value,
                                            notification_medium=mock_notification.notification_medium.value,
                                            message=mock_notification.message,
                                            sent_datetime=mock_notification.sent_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                            status=mock_notification.status.value)
    mock_azure_table_connector.get_entities.return_value = [stored_entity.__dict__]
    mock_azure_table_connector_class.return_value = mock_azure_table_connector
    get_notification_history = GetNotificationHistory(mock_azure_table_connector, mock_notification_history_adapter_config)
    expected_query_string = f"user_id eq '{mock_get_notification_history_request.user_id}'"

    # Act
    response = get_notification_history.get_notification_history(mock_get_notification_history_request)

    # Assert
    mock_azure_table_connector.get_entities.assert_called_once_with(
        table_name=mock_notification_history_adapter_config.notification_history_table_name,
        query_filter=expected_query_string
    )
    assert isinstance(response, GetNotificationHistoryResponse)
    assert response.status == AdapterOperationStatus.SUCCESS
    assert response.notifications == [mock_notification]


@patch('adapters.notification_history_adapter.store_notification_history.AzureTableConnector')
def test_get_notification_logs_error_on_exception(mock_azure_table_connector_class: MagicMock, 
                                                   mock_notification_history_adapter_config: NotificationHistoryAdapterConfig, 
                                                   mock_get_notification_history_request: GetNotificationHistoryRequest,
                                                   caplog: pytest.LogCaptureFixture):
    # Arrange
    mock_azure_table_connector = MagicMock() 
    mock_azure_table_connector.get_entities.side_effect = Exception("Failed to get entity")
    mock_azure_table_connector_class.return_value = mock_azure_table_connector
    adapter = GetNotificationHistory(mock_azure_table_connector, mock_notification_history_adapter_config)

    # Act
    with caplog.at_level('ERROR'):
        response = adapter.get_notification_history(mock_get_notification_history_request)

    # Assert
    assert "Failed to get notification history (notification history request: {'user_id': '123e4567-e89b-12d3-a456-426614174000', 'notification_type': None, 'notification_medium': None, 'start_date': None, 'end_date': None, 'status': None}) with error: Failed to get entity" in caplog.text
    assert isinstance(response, GetNotificationHistoryResponse)
    assert response.notifications == []
    assert response.message == "Failed to get notification history: Failed to get entity"
    assert response.status == AdapterOperationStatus.FAILED 


