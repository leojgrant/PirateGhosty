import pytest
import datetime
from unittest.mock import patch, MagicMock
from application.models.dtos.notification_dto import NotificationDto
from application.models.enums.notification_status import NotificationStatus
from tests.unit_tests.unit_test_config import unit_test_config
from application.models.enums.notification_medium import NotificationMedium
from application.models.enums.notification_types import NotificationTypes
from adapters.notification_history_adapter.delete_notification_history import DeleteNotificationHistory
from adapters.notification_history_adapter.notification_history_adapter_config import NotificationHistoryAdapterConfig
from adapters.notification_history_adapter.models.notification_history_table_entity import NotificationHistoryTableEntity
from application.models.requests.delete_notification_history_request import DeleteNotificationHistoryRequest
from application.models.enums.adapter_operation_status import AdapterOperationStatus
from application.models.responses.delete_notification_history_response import DeleteNotificationHistoryResponse

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
def mock_notification_entity(mock_notification):
    return NotificationHistoryTableEntity(PartitionKey=mock_notification.user_id, 
                                            RowKey="0", 
                                            user_id=mock_notification.user_id, 
                                            notification_type=mock_notification.notification_type.value,
                                            notification_medium=mock_notification.notification_medium.value,
                                            message=mock_notification.message,
                                            sent_datetime=mock_notification.sent_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                            status=mock_notification.status.value)

@pytest.fixture(scope='module')
def mock_delete_notification_history_request():
    return DeleteNotificationHistoryRequest()


######################## TESTS #######################

@patch('adapters.notification_history_adapter.store_notification_history.AzureTableConnector') 
def test_store_notification_history_success(mock_azure_table_connector_class: MagicMock, 
                                   mock_notification: NotificationDto,
                                   mock_notification_entity: NotificationHistoryTableEntity,
                                   mock_notification_history_adapter_config: NotificationHistoryAdapterConfig, 
                                   mock_delete_notification_history_request: DeleteNotificationHistoryRequest):
    
    # Arrange
    mock_azure_table_connector = MagicMock() 
    mock_azure_table_connector.get_entities.return_value = [mock_notification_entity.__dict__]
    mock_azure_table_connector_class.return_value = mock_azure_table_connector
    adapter = DeleteNotificationHistory(mock_azure_table_connector, mock_notification_history_adapter_config)

    # Act
    response = adapter.delete_notification_history(mock_delete_notification_history_request)

    # Assert
    mock_azure_table_connector.delete_entity.assert_called_once()
    mock_azure_table_connector.delete_entity.assert_called_once_with(
        table_name=mock_notification_history_adapter_config.notification_history_table_name,
        partition_key=mock_notification.user_id,
        row_key="0"
    )
    assert isinstance(response, DeleteNotificationHistoryResponse)
    assert response.status == AdapterOperationStatus.SUCCESS
    


@patch('adapters.notification_history_adapter.store_notification_history.AzureTableConnector')
def test_send_notification_logs_error_on_exception(mock_azure_table_connector_class: MagicMock, 
                                                   mock_notification_history_adapter_config: NotificationHistoryAdapterConfig, 
                                                   mock_delete_notification_history_request: DeleteNotificationHistoryRequest,
                                                   mock_notification_entity: NotificationHistoryTableEntity,
                                                   caplog: pytest.LogCaptureFixture):
    # Arrange
    mock_azure_table_connector = MagicMock() 
    mock_azure_table_connector.get_entities.return_value = [mock_notification_entity.__dict__]
    mock_azure_table_connector.delete_entity.side_effect = Exception("Failed to delete entity")
    mock_azure_table_connector_class.return_value = mock_azure_table_connector
    adapter = DeleteNotificationHistory(mock_azure_table_connector, mock_notification_history_adapter_config)

    # Act
    with caplog.at_level('ERROR'):
        response = adapter.delete_notification_history(mock_delete_notification_history_request)

    # Assert
    assert "Failed to delete notification history (notification history request: {'user_id': None, 'notification_type': None, 'notification_medium': None, 'start_date': None, 'end_date': None, 'status': None}) with error: Failed to delete entity" in caplog.text
    assert isinstance(response, DeleteNotificationHistoryResponse)
    assert response.message == "Failed to delete notification history: Failed to delete entity"
    assert response.status == AdapterOperationStatus.FAILED 


