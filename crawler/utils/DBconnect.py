import mysql.connector
from config import DB_CONFIG


def insert_rate(bank: str, currency: str, rate: float, timestamp) :
    try :
        # context manager로 mysql, cursor 열기 (자동 닫힘)
        with mysql.connector.connect(**DB_CONFIG) as conn :
            with conn.cursor() as cursor :
                sql = """
                    INSERT INTO exchange_rates (bank, currency, rate, timestamp)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE rate = VALUES(rate)
                """

                cursor.execute(sql, (bank, currency, rate, timestamp))
                conn.commit()
                print(f"[DB] 저장 성공 : {bank} {currency} {rate} {timestamp}")

    except Exception as e :
        print(f"[DB ERROR] {e}")
