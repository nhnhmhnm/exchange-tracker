from .ibk import get_ibk
from .shinhan import get_shinhan
from utils.enums import Bank, Currency

def get_rate(bank: Bank, currency: Currency) -> dict | None:
    if bank == Bank.IBK:
        return get_ibk(currency)
    elif bank == Bank.SHINHAN:
        return get_shinhan(currency)
    else:
        print(f"[ERROR] 미지원 은행: {bank}")
        return None
