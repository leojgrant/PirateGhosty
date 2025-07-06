import pytest
import datetime
from tests.integration_tests.integration_test_config import integration_test_config
from adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter import WhatsappNotificationsAdapter
from application.models.dtos.notification_dto import NotificationDto
from application.models.responses.notification_response import NotificationResponse
from application.models.enums.notification_status import NotificationStatus
from adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter_config import WhatsappNotificationsAdapterConfig
from application.models.enums.notification_medium import NotificationMedium
from application.models.enums.notification_types import NotificationTypes
from application.models.requests.whatsapp_notification_request import WhatsappNotificationRequest


####################### MOCKS #######################

@pytest.fixture(scope='module')
def notification_adapter_config(integration_test_config):
        return integration_test_config

@pytest.fixture(scope='module')
def bad_notification_adapter_config(integration_test_config):
        integration_test_config.twilio_account_sid = "broken_account_sid",
        integration_test_config.twilio_auth_token = "broken_auth_token",
        integration_test_config.twilio_whatsapp_number = "broken_whatsapp_number"
        return integration_test_config

@pytest.fixture(scope='module')
def mock_notification():
    return NotificationDto(
        user_id='user123',
        notification_medium=NotificationMedium.WHATSAPP,
        notification_type=NotificationTypes.LEE_VALLEY_TENNIS_BOOKING_ALERT,
        message='Test notification for user123',
    )

@pytest.fixture(scope='module')
def mock_whatsapp_notification_request(integration_test_config, mock_notification):
    return WhatsappNotificationRequest(
        notification = mock_notification,
        phone_number=integration_test_config.test_target_whatsapp_number,
    )

######################## TESTS #######################

def test_send_notification_success(notification_adapter_config: WhatsappNotificationsAdapterConfig, 
                                   mock_whatsapp_notification_request: WhatsappNotificationRequest):
    
    # Arrange
    adapter = WhatsappNotificationsAdapter(notification_adapter_config)

    # Act
    try:
        response = adapter.send_notification(mock_whatsapp_notification_request)

        # Assert
        assert isinstance(response, NotificationResponse)
        assert response.user_id == mock_whatsapp_notification_request.notification.user_id
        assert response.status == NotificationStatus.SENT
        assert response.message == "Notification sent successfully."
    except Exception as e:
        pytest.fail(f"test_send_notification_success failed. Send_notification() raised an unexpected exception: {e}")


def test_send_notification_bad_config(bad_notification_adapter_config: WhatsappNotificationsAdapterConfig, 
                                   mock_whatsapp_notification_request: WhatsappNotificationRequest):
    
    # Arrange
    adapter = WhatsappNotificationsAdapter(bad_notification_adapter_config)

    # Act
    try:
        response = adapter.send_notification(mock_whatsapp_notification_request)

        # Assert
        assert isinstance(response, NotificationResponse)
        assert response.user_id == mock_whatsapp_notification_request.notification.user_id
        assert response.status == NotificationStatus.FAILED
    except Exception as e:
        pytest.fail(f"test_send_notification_bad_config failed. Send_notification() raised an unexpected exception: {e}")

