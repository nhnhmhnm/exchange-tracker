from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import CHROME_DRIVER_PATH
from datetime import datetime

from banks.enums import Bank, Currency

def get_ibk(currency: Currency) -> dict | None :
    url = "https://www.ibk.co.kr/fxtr/excRateList.ibk?pageId=SM03020100"

    options = Options()
    options.add_argument("--headless")

    try :
        service = Service(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)

        # 고시완료 시각
        # 성공하면 시각 파싱 후 저장, 실패하면 현재 시각 저장
        try :
            time_tag = driver.find_element(By.CLASS_NAME, "standard")
            time_text = time_tag.text.split()[3]
            print(f"[INFO] IBK {time_text}")

            # 파싱
            time_str = time_text.split(":")[-1].strip()
            now = datetime.now().replace(
                hour=int(time_str[0:2]),
                minute=int(time_str[3:5]),
                second=int(time_str[6:8]),
                microsecond=0
            )

        except Exception as e :
            now = datetime.now()
            print(f"[WARN] IBK 고시완료 시각 파싱 실패 {e}")

        # 매매기준율
        table = driver.find_element(By.CLASS_NAME, "tbl_basic")
        rows = table.find_elements(By.TAG_NAME, "tr")
        print(f"[INFO] IBK 테이블 로드 성공")

        for row in rows :
            ths = row.find_elements(By.TAG_NAME, "th") # 통화

            if ths and currency.value in ths[0].text :
                tds = row.find_elements(By.TAG_NAME, "td") # 매매기준율

                if len(tds) >= 1 :
                    rate_text = tds[0].text.strip().replace(",", "")
                    rate = float(rate_text)
                    print(f"[INFO] IBK {currency.value} 매매기준율: {rate}")

                    return {
                        "bank": Bank.IBK.value,
                        "currency": currency.value,
                        "rate": rate,
                        "timestamp": now
                    }

        print(f"[WARN] IBK {currency.value} 데이터를 찾지 못함")

    except Exception as e :
        print(f"[ERROR] get_ibk 실패: {e}")

    finally :
        try :
            driver.quit()
        except :
            pass

    return None
