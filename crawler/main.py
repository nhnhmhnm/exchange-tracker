from banks.ibk import get_ibk_usd_rate
from utils.DBconnect import insert_rate
from datetime import datetime

def crawl_ibk():
    result = get_ibk_usd_rate()
    if result:
        insert_rate(
            bank=result["bank"],
            currency=result["currency"],
            rate=result["rate"],
            timestamp=result["timestamp"]
        )
    else:
        print(f"[{datetime.now()}] main IBK 크롤링 실패")

if __name__ == "__main__":
    crawl_ibk()
