from enum import Enum

class Bank(str, Enum):
    IBK = "IBK"
    SHINHAN = "SHINHAN"
    
class Currency(str, Enum):
    USD = "USD"
    JPY = "JPY"
