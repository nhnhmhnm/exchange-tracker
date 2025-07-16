import mysql.connector
from config import DB_CONFIG
from utils.enums import Bank, Currency

def get_foreign_key_id(cursor, table: str, code: str) -> int:
    sql = f"SELECT id FROM {table} WHERE code = %s"
    cursor.execute(sql, (code,))
    result = cursor.fetchone()
    if result is None:
        raise ValueError(f"{table}에서 code='{code}'를 찾을 수 없습니다.")
    return result[0]

def insert_rate(bank: Bank, currency: Currency, rate: float, timestamp):
    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # bank_id, currency_id 조회
                bank_id = get_foreign_key_id(cursor, "banks", bank.value)
                currency_id = get_foreign_key_id(cursor, "currencies", currency.value)


                # INSERT
                sql = """
                    INSERT INTO exchange_rates (bank_id, currency_id, rate, timestamp)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE rate = VALUES(rate)
                """
                cursor.execute(sql, (bank_id, currency_id, rate, timestamp))
                conn.commit()

                print(f"[DB] 저장 성공 : {bank.value} {currency.value} {rate} {timestamp}")

    except Exception as e:
        print(f"[DB ERROR] {e}")

# def insert_rate(bank: str, currency: str, rate: float, timestamp) :
#     try:
#         # context manager로 mysql, cursor 열기 (자동 닫힘)
#         with mysql.connector.connect(**DB_CONFIG) as conn:
#             with conn.cursor() as cursor:
#                 sql = """
#                     INSERT INTO exchange_rates (bank, currency, rate, timestamp)
#                     VALUES (%s, %s, %s, %s)
#                     ON DUPLICATE KEY UPDATE rate = VALUES(rate)
#                 """

#                 cursor.execute(sql, (bank, currency, rate, timestamp))
#                 conn.commit()
#                 print(f"[DB] 저장 성공 : {bank} {currency} {rate} {timestamp}")

#     except Exception as e:
#         print(f"[DB ERROR] {e}")
