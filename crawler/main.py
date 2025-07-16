from banks.ibk import get_ibk
from banks.shinhan import get_shinhan
from utils.crawler import crawl_all
from utils.DBconnect import insert_rate
from utils.enums import Bank, Currency

if __name__ == "__main__":
    crawl_all()
