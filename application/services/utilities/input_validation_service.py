import uuid

class InputValidationService:        
    @staticmethod
    def is_valid_uuid(uuid_string: str) -> bool:
        try:
            uuid.UUID(uuid_string)
            return True
        except Exception:
            return False 