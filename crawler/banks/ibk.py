from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import CHROME_DRIVER_PATH
from datetime import datetime

def get_ibk_usd_rate() -> dict | None:
    url = "https://www.ibk.co.kr/fxtr/excRateList.ibk?pageId=SM03020100"

    options = Options()
    options.add_argument("--headless")

    try:
        service = Service(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        print("[INFO] 드라이버 실행 성공")

        driver.get(url)
        print("[INFO] 페이지 로드 성공")

        try:
            time_tag = driver.find_element(By.CLASS_NAME, "standard")  # 또는 By.XPATH
            time_text = time_tag.text.strip()  # "고시완료 시각 : 11:15:23"
            print(f"[INFO] 시간 태그 내용: {time_text}")

            time_str = time_text.split(":")[-1].strip()  # '11:15:23'
            now = datetime.now().replace(
                hour=int(time_str[0:2]),
                minute=int(time_str[3:5]),
                second=int(time_str[6:8]),
                microsecond=0
            )
        except Exception as e:
            now = datetime.now()
            print(f"[WARN] 고시 시각 파싱 실패, fallback 사용: {e}")


        table = driver.find_element(By.CLASS_NAME, "tbl_basic")
        rows = table.find_elements(By.TAG_NAME, "tr")
        print(f"[INFO] 테이블 로드 성공, 행 수: {len(rows)}")

        for row in rows:
            ths = row.find_elements(By.TAG_NAME, "th")
            if ths and "USD" in ths[0].text:
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(tds) >= 1:
                    rate_text = tds[0].text.strip().replace(",", "")
                    rate = float(rate_text)
                    print(f"[INFO] USD 매매기준율: {rate}")
                    return {
                        "bank": "IBK기업은행",
                        "currency": "USD",
                        "rate": rate,
                        "timestamp": now
                    }

        print("[WARN] USD 데이터를 찾지 못함")

    except Exception as e:
        print(f"[ERROR] get_ibk_usd_rate 실패:", e)
    finally:
        try:
            driver.quit()
        except:
            pass

    return None
