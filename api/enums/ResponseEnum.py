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
    # File upload responses
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_FAILURE = "File upload failed"
    # File processing responses
    FILE_PROCESSING_SUCCESS = "File processed successfully"
    FILE_PROCESSING_FAILURE = "File processing failed"
    #loader responses
    LOADER_INITIALIZATION_SUCCESS = "Loader initialized successfully"
    LOADER_INITIALIZATION_FAILURE = "Loader initialization failed"
    # No files to process
    FILE_NOT_FOUND = "File not found in the specified folder"
    FILE_ID_NOT_FOUND = "File ID not found in the specified folder"
    NO_FILES_TO_PROCESS = "No files found to process"
    
    