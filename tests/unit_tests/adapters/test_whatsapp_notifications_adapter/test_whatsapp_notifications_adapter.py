import pytest
from unittest.mock import patch, MagicMock
from adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter import WhatsappNotificationsAdapter 
from application.models.dtos.notification_dto import NotificationDto
from adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter_config import WhatsappNotificationsAdapterConfig
from application.models.enums.notification_status import NotificationStatus
from tests.unit_tests.unit_test_config import unit_test_config
from application.models.enums.notification_medium import NotificationMedium
from application.models.enums.notification_types import NotificationTypes
from application.models.requests.whatsapp_notification_request import WhatsappNotificationRequest

####################### MOCKS #######################

@pytest.fixture(scope='module')
def mock_notification_adapter_config(unit_test_config):
    unit_test_config.twilio_account_sid = 'test_sid'
    unit_test_config.twilio_auth_token = 'test_token'
    unit_test_config.twilio_whatsapp_number = '1234567890'
    return unit_test_config

@pytest.fixture(scope='module')
def mock_notification():
    return NotificationDto(
        user_id='user123',
        notification_medium=NotificationMedium.WHATSAPP,
        notification_type=NotificationTypes.LEE_VALLEY_TENNIS_BOOKING_ALERT,
        message='Test notification for user123',
        status=NotificationStatus.UNDELIVERED,
        sent_datetime=None 
    )

@pytest.fixture(scope='module')
def mock_whatsapp_notification_request(mock_notification):
    return WhatsappNotificationRequest(
        notification = mock_notification,
        phone_number="9876543210",
    )

######################## TESTS #######################

@patch('adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter.Client') # Replace 'Client' import in notifications_adapter.py with a mocked object
def test_send_notification_success(mock_twilio_client_class: MagicMock, # The mocked twilio 'Client' class imported from notifications_adapter.py
                                   mock_notification_adapter_config: WhatsappNotificationsAdapterConfig, 
                                   mock_whatsapp_notification_request: WhatsappNotificationRequest):
    
    # Arrange
    mock_twilio_client = MagicMock() # The item to be returned when the mocked 'Client' class is called
    mock_twilio_response = MagicMock()
    mock_twilio_response.status = NotificationStatus("sent")
    mock_twilio_client.messages.create.return_value = mock_twilio_response
    mock_twilio_client_class.return_value = mock_twilio_client
    adapter = WhatsappNotificationsAdapter(mock_notification_adapter_config)

    # Act
    adapter.send_notification(mock_whatsapp_notification_request)

    # Assert
    mock_twilio_client.messages.create.assert_called_once_with(
        from_='whatsapp:+1234567890',
        body='Test notification for user123',
        to='whatsapp:+9876543210'
    )


@patch('adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter.Client')
def test_send_notification_logs_error_on_exception(mock_twilio_client_class: MagicMock, 
                                                   mock_notification_adapter_config: WhatsappNotificationsAdapterConfig, 
                                                   mock_whatsapp_notification_request: WhatsappNotificationRequest,
                                                   caplog: pytest.LogCaptureFixture): # caplog is a part of pytest that captures log messages
    # Arrange
    mock_twilio_client = MagicMock()
    mock_twilio_client.messages.create.side_effect = Exception("Twilio exploded")
    mock_twilio_client_class.return_value = mock_twilio_client

    adapter = WhatsappNotificationsAdapter(mock_notification_adapter_config)

    # Act
    with caplog.at_level('ERROR'):
        adapter.send_notification(mock_whatsapp_notification_request)

    # Assert
    assert "Failed to send whatsapp notification to (notification: {'user_id': 'user123', 'notification_type': <NotificationTypes.LEE_VALLEY_TENNIS_BOOKING_ALERT: 'lee_valley_tennis_booking_alert'>, 'notification_medium': <NotificationMedium.WHATSAPP: 'whatsapp'>, 'message': 'Test notification for user123', 'status': <NotificationStatus.UNDELIVERED: 'undelivered'>, 'sent_datetime': None}) to (phone number: 9876543210) with error: Twilio exploded" in caplog.text

