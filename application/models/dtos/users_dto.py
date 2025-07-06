class UsersDto:
    """
    Users Dto Structure for the application layer
    """
    def __init__(self, user_id: str, username: str, phone_number: str):
        """
        Initializes the user DTO.

        :param user_id: The unique identifier for the user.
        :param username: The username of the user.
        :param phone_number: The phone number of the user.
        """
        self.user_id = user_id
        self.username = username
        self.phone_number = phone_number