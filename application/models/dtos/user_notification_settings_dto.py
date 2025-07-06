class UserNotificationSettingsDto:
    """
    user Notification Settings Table Data Structure (for the application layer)
    """
    def __init__(self, user_id: str, booking_weekday: str, booking_time: str):
        """
        Initializes the Notification History Table Dto.

        :param user_id: The user_id associated with the notification settings.
        :param booking_weekday: The weekday of the booking associated with the notification settings.
        :param booking_time: The date of the booking in the notification.
        """
        self.user_id = user_id
        self.booking_day = booking_weekday
        self.booking_time = booking_time