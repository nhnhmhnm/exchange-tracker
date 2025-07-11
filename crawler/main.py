from banks.ibk import get_ibk
from banks.enums import Currency
from utils.DBconnect import insert_rate

def crawl_ibk():
    for currency in Currency :
        rates = get_ibk(currency)

        if rates :
            insert_rate(**rates)
            print(f"[SUCCESS] {currency.value} 저장 완료")
        else:
            print(f"[FAIL] {currency.value} 저장 실패")

if __name__ == "__main__" :
    crawl_ibk()
