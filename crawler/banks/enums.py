from enum import Enum

class Bank(str, Enum):
    IBK = "IBK기업은행"
    
class Currency(str, Enum):
    USD = "USD"
    JPY = "JPY"
