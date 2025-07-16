from banks.common import get_rate
from utils.enums import Bank, Currency
from utils.DBconnect import insert_rate

def crawl_all():
    for bank in Bank:
        for currency in Currency:
            try:
                result = get_rate(bank, currency)

                if result is None:
                    print(f"[WARN] {bank.value} {currency.value} 크롤링 실패")
                else:
                    insert_rate(**result)
                    print(f"[SUCCESS] {bank.value} {currency.value} 저장 완료")
            except Exception as e:
                print(f"[ERROR] {bank.value} {currency.value} 예외 발생: {e}")
