import schedule
import time
from main import crawl_ibk

# 10분마다 실행
schedule.every(10).minutes.do(crawl_ibk)

print("[시작] IBK기업은행 USD 환율 크롤러")

crawl_ibk()  # 최초 실행

while True:
    schedule.run_pending()
    time.sleep(1)
