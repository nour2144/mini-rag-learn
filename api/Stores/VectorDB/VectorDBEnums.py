from enum import Enum

class VectorDBEnum(Enum):
    QDRANT = "qdrant"
    MODE_ONLINE = "online"
    MODE_OFFLINE = "offline"

class DistanceMethodEnum(Enum):
    COSINE = "cosine"
    DOT = "dot"