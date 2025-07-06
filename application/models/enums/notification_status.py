from enum import Enum

class NotificationStatus(Enum):
    UNDELIVERED = "undelivered"
    SENT = "sent"
    FAILED = "failed"