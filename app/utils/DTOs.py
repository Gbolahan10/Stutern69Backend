from enum import Enum

class ConnectRole(Enum):
    PERSONAL = "PERSONAL"
    PROFESSIONAL = "PROFESSIONAL"

class CommunityRole(Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    MEMBER = "MEMBER"

class CommunityType(Enum):
    GROUP = "GROUP"
    CHANNEL = "CHANNEL"
