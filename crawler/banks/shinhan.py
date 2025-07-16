import requests
from datetime import datetime
from enum import Enum
from utils.enums import Currency, Bank


def get_shinhan(currency: Currency) -> dict | None:
    url = "https://bank.shinhan.com/serviceEndpoint/httpDigital"

    payload = {
        "dataBody": {
            "ricInptRootInfo": {
                "serviceType": "GU",
                "serviceCode": "F3733",
                "callBack": "shbObj.fncF3733Callback",
                "webUri": "/index.jsp",
                "isRule": "N"
            },
            "조회구분": "",
            "조회일자": datetime.now().strftime("%Y%m%d"),
            "고시회차": ""
        },
        "dataHeader": {
            "trxCd": "RSRFO0100A01",
            "language": "ko",
            "subChannel": "49",
            "channelGbn": "D0"
        }
    }

    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        data = res.json()
    
        # 고시시간
        date_str = data["dataBody"]["고시일자_display"]
        time_str = data["dataBody"]["고시시간_display"]
        datetime_str = f"{date_str} {time_str}"
        
        timestamp = datetime.strptime(datetime_str, "%Y.%m.%d %H:%M:%S")

        # 통화
        rates = data["dataBody"]["R_RIBF3733_1"]

        for rate in rates:
            if rate["통화CODE"] == currency.value:
                base_rate = float(rate["매매기준환율"])
                print(f"[INFO] SHINHAN {currency.value} 매매기준율: {base_rate}")

                return {
                    "bank": Bank.SHINHAN,
                    "currency": currency,
                    "rate": base_rate,
                    "timestamp": timestamp
                }

        print(f"[WARN] SHINHAN {currency.value} 데이터를 찾지 못함")

    except Exception as e:
        print(f"[ERROR] get_shinhan 실패: {e}")

    return None
