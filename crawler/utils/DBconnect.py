import mysql.connector
from config import DB_CONFIG


def insert_rate(bank: str, currency: str, rate: float, timestamp):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = """
            INSERT INTO exchange_rates (bank, currency, rate, timestamp)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE rate = VALUES(rate)
        """
        cursor.execute(sql, (bank, currency, rate, timestamp))
        conn.commit()

        print(f"[DB] 저장 성공 : {bank} {currency} {rate} {timestamp}")

    except Exception as e:
        print(f"[DB ERROR] {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
