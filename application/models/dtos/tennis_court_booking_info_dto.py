import datetime

class TennisCourtBookingInfoDto:
    def __init__(self, start_time: datetime, end_time: datetime, number_of_available_courts: int):
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_available_courts = number_of_available_courts

    # N.B. Use __repr__ for clear representation (debugging, dev purposes)
    def __repr__(self):
        return f"TennisCourtBookingDto(start_time='{self.start_time}', end_time='{self.end_time}', number_of_available_courts={self.number_of_available_courts})"
    
    # N.B. Use __str__ for user-friendly representation (user-facing)
    def __str__(self):
        return f"Available courts from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')}: {self.number_of_available_courts} courts"