from twilio.rest import Client
from application.models.responses.notification_response import NotificationResponse
from adapters.whatsapp_notifications_adapter.whatsapp_notifications_adapter_config import WhatsappNotificationsAdapterConfig
from application.models.enums.notification_status import NotificationStatus
from application.models.requests.whatsapp_notification_request import WhatsappNotificationRequest
import logging

class WhatsappNotificationsAdapter:
    """
    Class for the whatsapp notifications adapters.
    """

    def __init__(self, whatsapp_notifications_adapter_config: WhatsappNotificationsAdapterConfig):
        """
        Initializes the WhatsappNotificationsAdapter.

        :param notifications_adapter_config: The configuration for the notifications adapter.
        """
        self.notifications_adapter_config = whatsapp_notifications_adapter_config
        self.twilio_client = Client(whatsapp_notifications_adapter_config.twilio_account_sid, whatsapp_notifications_adapter_config.twilio_auth_token)


    def send_notification(self, request: WhatsappNotificationRequest) -> NotificationResponse:
        """
        Send a notification.

        :param notification: The notfication to be sent.
        """
        try:
            logging.info(f"Sending whatsapp notification to user_id: {request.notification.user_id}.")
            twilio_response = self.twilio_client.messages.create(
                from_=f"whatsapp:+{self.notifications_adapter_config.twilio_whatsapp_number}",
                body=request.notification.message,
                to=f"whatsapp:+{request.phone_number}"
            )
            return NotificationResponse(
                user_id=request.notification.user_id,
                status=NotificationStatus.SENT,
                message=twilio_response.error_message if twilio_response.error_message else "Notification sent successfully.",
            )
        except Exception as e:
            logging.error(f"Failed to send whatsapp notification to (notification: {request.notification.__dict__}) to (phone number: {request.phone_number}) with error: {e}")
            return NotificationResponse(
                user_id=request.notification.user_id,
                status=NotificationStatus.FAILED,
                message=f"Failed to send notification: {str(e)}"
            )
        