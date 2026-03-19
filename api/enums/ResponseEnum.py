from enum import Enum

class ResponseEnum(Enum):
    # General responses
    BASE_SUCCESS = "Base work successfully"
    BASE_FAILURE = "Base work failed"
    # File validation responses
    FILE_VALIDATION_SUCCESS = "File validation successful"
    FILE_VALIDATION_FAILURE = "File validation failed"
    FILE_TYPE_UNSUPPORTED = "Unsupported file type"
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum allowed size"
    